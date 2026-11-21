"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm Randomss (file nộp).
Chạy trong thư mục src/: python lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
Mọi con số tính từ cột *_simulated được in kèm nhãn [simulated].
"""
import math
import sys
from statistics import NormalDist

import pandas as pd

# In tiếng Việt đúng trên console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)
CO_DINH_THANG = 40_000_000   # chi phí cố định của trợ lý, đồng / tháng
YC_THANG = 45_000            # yêu cầu hoàn phí mỗi tháng ở quy mô đầy đủ
PHAM_VI = ['noi_dia', 'hang_nang']   # phạm vi pilot đề xuất (dựa trên A3)
SIM = '[simulated]'


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng.
    Lần thứ i được chạy khi i-1 lần trước đều sai: tổng (1-p)^(i-1), i = 1..k."""
    if k is None:
        return 1 / p
    return (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    if k is None:
        return 1.0
    return 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')
    print(f'  so_lan_chay_ky_vong(0.8, 2)               = {so_lan_chay_ky_vong(0.8, 2):.2f}')
    print(f'  so_lan_chay_ky_vong(0.8)                  = {so_lan_chay_ky_vong(0.8):.2f}')
    print(f'  he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) = {he_so_chi_phi_moi_viec_thanh_cong(0.8, 3):.2f}')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, chay_lai, xem_lai, lam_lai, tong, thanh_cong, cps, hoa_don_moi_yc.
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × luong_phut. Đây là số GIẢ LẬP.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong' (mẫu số).
    - max_lan_chay: bỏ lần chạy có attempt > giới hạn; yêu cầu có so_lan_chay > giới hạn
      coi là chuyen_nhan_vien, phút xem lại và làm lại bằng 0.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(token=tien_token.sum(),
                tool=tien_tool.sum(),
                chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
                xem_lai=xem_lai,
                lam_lai=lam_lai,
                tong=tong,
                thanh_cong=thanh_cong,
                cps=tong / thanh_cong,
                hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs))


# ---------- Nhiệm vụ D1 · Cỡ mẫu ----------
def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ (công thức có p̄ ở vế alpha)."""
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def he_so_thiet_ke(m, icc):
    return 1 + (m - 1) * icc


def co_mau_hieu_dung(c, m, icc):
    return c * m / he_so_thiet_ke(m, icc)


def tieu_de(ten):
    print()
    print('=' * 78)
    print(ten)
    print('=' * 78)


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)

    # ---------------- A1 ----------------
    tieu_de('A1 · Ba phép thử đáp án biết trước')
    kiem_tra_dap_an_biet_truoc()

    # ---------------- A2 ----------------
    tieu_de('A2 · Mô hình chi phí từ trace (1.200 yêu cầu)')
    goc = mo_hinh(runs, reqs)
    nhan = dict(token='đo từ trace', tool='đo từ trace', chay_lai='đo từ trace',
                xem_lai=SIM, lam_lai=SIM, tong='có phần ' + SIM, thanh_cong='',
                cps=SIM, hoa_don_moi_yc='đo từ trace')
    for ten, gia_tri in goc.items():
        print(f'{ten:15s} {gia_tri:>14,.1f}  {nhan[ten]}')
    print(f'Số lần gọi tool: {runs.tool_calls.sum():,} · phút xem lại: {reqs.phut_xem_lai_simulated.sum():,} '
          f'· phút làm lại: {reqs.phut_lam_lai_simulated.sum():,} {SIM}')
    print(f'CPS / hoá đơn mỗi yêu cầu = {goc["cps"] / goc["hoa_don_moi_yc"]:.1f} lần')
    for k in ['token', 'tool', 'xem_lai', 'lam_lai']:
        print(f'  Tỉ trọng {k:8s}: {goc[k] / goc["tong"] * 100:5.1f}%')
    print(f'  Giờ nhân viên (xem lại + làm lại): {(goc["xem_lai"] + goc["lam_lai"]) / goc["tong"] * 100:.1f}% {SIM}')
    khong_tc = len(reqs) - goc['thanh_cong']
    he_thong = (goc['tong'] + khong_tc * BASELINE) / len(reqs)
    print(f'Chi phí cả hệ thống mỗi yêu cầu (cộng {khong_tc} ca không thành công × 12.000 đ): '
          f'{he_thong:,.0f} đ = {he_thong / BASELINE:.2f}× {SIM}')
    print(reqs.ket_qua.value_counts().to_string())

    # Kiểm tra tay một con số (vai người kiểm số)
    token_tay = (runs.tokens_in.sum() / 1000 * GIA_VAO + runs.tokens_out.sum() / 1000 * GIA_RA)
    print(f'Kiểm tay: token = {runs.tokens_in.sum():,}/1000×26 + {runs.tokens_out.sum():,}/1000×130 = {token_tay:,.1f} đ')

    # ---------------- A3 ----------------
    tieu_de('A3 · Tách theo loại yêu cầu')
    print(f'{"loai":10s} {"so_yc":>6s} {"ti_le_tc":>9s} {"lan/yc":>7s} {"cps [sim]":>10s} {"so 12k":>7s}')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        r = reqs[reqs.loai == loai]
        kq = mo_hinh(runs, r)
        so_lan = runs[runs.request_id.isin(r.request_id)].shape[0] / len(r)
        print(f'{loai:10s} {len(r):6d} {kq["thanh_cong"] / len(r) * 100:8.1f}% {so_lan:7.2f} '
              f'{kq["cps"]:10,.0f} {kq["cps"] / BASELINE:6.2f}×')
    ok_theo_lan = (runs.merge(reqs[['request_id', 'loai']], on='request_id')
                   .assign(ok=lambda d: (d.status == 'ok').astype(float))
                   .pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean'))
    print('\nTỉ lệ ok theo lần thử (attempt):')
    print((ok_theo_lan * 100).round(1).to_string())

    # ---------------- A4 ----------------
    tieu_de('A4 · Chi phí cố định 40 triệu đ/tháng, phạm vi noi_dia + hang_nang')
    r_pv = reqs[reqs.loai.isin(PHAM_VI)]
    pv = mo_hinh(runs, r_pv)
    cps_pv = pv['tong'] / pv['thanh_cong']
    print(f'Phạm vi: {len(r_pv)} yêu cầu, {pv["thanh_cong"]} thành công, tổng {pv["tong"]:,.0f} đ, '
          f'CPS {cps_pv:,.0f} đ {SIM}')
    for ten, he_so in [('45.000 yc/tháng', 1.0), ('Một nửa khối lượng', 0.5)]:
        tc_thang = YC_THANG * he_so * pv['thanh_cong'] / len(reqs)
        co_dinh = CO_DINH_THANG / tc_thang
        print(f'{ten:20s} việc TC/tháng {tc_thang:9,.0f} · cố định/việc {co_dinh:6,.0f} đ · '
              f'CPS + cố định {cps_pv + co_dinh:6,.0f} đ = {(cps_pv + co_dinh) / BASELINE:.2f}× {SIM}')

    # ---------------- B1 ----------------
    tieu_de('B1 · Đổi từng yếu tố (cả 1.200 yêu cầu)')
    kich_ban = {
        'Giá token gấp đôi':          dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa':     dict(gia_vao=13, gia_ra=65),
        'Tỉ lệ xem lại gấp đôi':      dict(he_so_xem_lai=2),
        'Tỉ lệ xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
        'Số ca làm lại gấp đôi':      dict(he_so_lam_lai=2),
        'Số ca làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
        'Lương nhân viên tăng 25%':   dict(luong_phut=2500),
        'Chỉ cho chạy tối đa 2 lần':  dict(max_lan_chay=2),
        'Chỉ cho chạy 1 lần':         dict(max_lan_chay=1),
    }
    print(f'{"Gốc (A2)":28s} {goc["cps"]:8,.0f} đ {SIM}')
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f'{ten:28s} {cps:8,.0f} đ {(cps / goc["cps"] - 1) * 100:+6.1f}%  {SIM}')

    # ---------------- B2 ----------------
    tieu_de('B2 · Đổi một cặp')
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    print(f'Giá token ×2 + xem lại ×2: {cap:,.0f} đ ({(cap / goc["cps"] - 1) * 100:+.1f}%) {SIM}')

    # ---------------- B3 ----------------
    tieu_de('B3 · Giới hạn chạy lại và chi phí cả hệ thống (1.200 yêu cầu)')
    for k in [1, 2, 3]:
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong = len(reqs) - kq['thanh_cong']
        print(f'Tối đa {k} lần: trợ lý {kq["tong"]:12,.0f} đ · không TC {khong:4d} · '
              f'cả hệ thống {kq["tong"] + khong * BASELINE:12,.0f} đ · CPS {kq["cps"]:6,.0f} đ {SIM}')

    # ---------------- B4 ----------------
    tieu_de('B4 · Xem lại 100% cho noi_dia + hang_nang')
    runs_pv = runs[runs.request_id.isin(r_pv.request_id)]
    co_ok = runs_pv[runs_pv.status == 'ok'].request_id.nunique()
    so_lam_lai = int((r_pv.ket_qua == 'lam_lai').sum())
    token_tool_pv = (runs_pv.tokens_in / 1000 * GIA_VAO + runs_pv.tokens_out / 1000 * GIA_RA
                     + runs_pv.tool_calls * GIA_TOOL).sum()
    phut_lam_lai_tb = reqs.loc[reqs.ket_qua == 'lam_lai', 'phut_lam_lai_simulated']
    for nhan_phut, phut_ll in [('9 phút (đề cho)', 9.0),
                               (f'{phut_lam_lai_tb.mean():.1f} phút (TB dữ liệu)', round(phut_lam_lai_tb.mean(), 1))]:
        tien_xem = co_ok * 5 * LUONG_PHUT
        tien_ll = so_lam_lai * phut_ll * LUONG_PHUT
        tong_b4 = token_tool_pv + tien_xem + tien_ll
        cps_b4 = tong_b4 / pv['thanh_cong']
        hoa_von = (BASELINE * pv['thanh_cong'] - token_tool_pv - tien_ll) / (co_ok * LUONG_PHUT)
        print(f'Làm lại {nhan_phut}: {co_ok} yc có ok × 5 phút = {tien_xem:,.0f} đ · '
              f'{so_lam_lai} ca làm lại = {tien_ll:,.0f} đ · token+tool {token_tool_pv:,.0f} đ')
        print(f'   tổng {tong_b4:,.0f} đ / {pv["thanh_cong"]} = {cps_b4:,.0f} đ = {cps_b4 / BASELINE:.2f}× {SIM}; '
              f'hoà vốn khi xem lại ≤ {hoa_von:.1f} phút/yc; tiền xem lại = {tien_xem / tong_b4 * 100:.0f}% tổng')
    print(f'Phút làm lại mỗi ca lam_lai: TB {phut_lam_lai_tb.mean():.1f}, trung vị {phut_lam_lai_tb.median():.1f} {SIM}')

    # ---------------- D1 ----------------
    tieu_de('D1 · Cỡ mẫu (baseline 0,70; +5 điểm; alpha 0,05; power 0,8; ICC 0,02)')
    ICC = 0.02
    n_a = co_mau(0.70, 0.75)
    print(f'a) Chia theo yêu cầu: {n_a:,} yêu cầu mỗi nhóm')
    de_b = he_so_thiet_ke(75, ICC)
    n_b = math.ceil(n_a * de_b)
    nv_b = math.ceil(n_b / 75)
    print(f'b) Theo nhân viên, m = 75: DE = {de_b:.2f}; n = {n_b:,} mỗi nhóm → {nv_b} NV mỗi nhóm, '
          f'tổng {2 * nv_b} > 40 → không đủ người')
    print(f'c) 20 NV mỗi nhóm: n hiệu dụng tối đa = 20 / {ICC} = {20 / ICC:,.0f} < {n_a:,} → không đạt')
    print(f'd) 6 depot mỗi nhóm: n hiệu dụng tối đa = 6 / {ICC} = {6 / ICC:,.0f}')
    n_6 = co_mau(0.70, 0.76)
    m_e = math.ceil(n_6 * (1 - ICC) / (20 - n_6 * ICC))
    print(f'e) Mức chênh 6 điểm: {n_6} mỗi nhóm; 20m / (1 + (m-1)·0,02) ≥ {n_6} → m ≥ {m_e} '
          f'yêu cầu mỗi NV (DE {he_so_thiet_ke(m_e, ICC):.2f}, n hiệu dụng {co_mau_hieu_dung(20, m_e, ICC):,.1f})')
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize
    pw5 = NormalIndPower().power(effect_size=proportion_effectsize(0.75, 0.70), nobs1=n_6, alpha=0.05)
    n_sm = NormalIndPower().solve_power(effect_size=proportion_effectsize(0.75, 0.70), alpha=0.05, power=0.8)
    print(f'Kiểm tra bằng statsmodels: n (5 điểm) ≈ {n_sm:,.0f}; với n = {n_6} mà tác động thật 5 điểm, power ≈ {pw5:.2f}')
    print(f'Mức sử dụng hiện tại: {reqs.staff_id.nunique()} NV trong mẫu, '
          f'TB {len(reqs) / reqs.staff_id.nunique():.0f} yc/NV trong 2 tuần ở {reqs.depot.nunique()} depot')

    # ---------------- Tỉ lệ an toàn hiện tại (trước khi đặt luật dừng) ----------------
    tieu_de('D3 · Tỉ lệ mo_lai_trong_7_ngay hiện tại')
    print(f'Toàn bộ: {reqs.mo_lai_trong_7_ngay.mean() * 100:.2f}% ({reqs.mo_lai_trong_7_ngay.sum()}/{len(reqs)})')
    print(f'Phạm vi noi_dia + hang_nang: {r_pv.mo_lai_trong_7_ngay.mean() * 100:.2f}% '
          f'({r_pv.mo_lai_trong_7_ngay.sum()}/{len(r_pv)})')
    print(f'Tỉ lệ lam_lai trong phạm vi: {(r_pv.ket_qua == "lam_lai").mean() * 100:.1f}% ({so_lam_lai}/{len(r_pv)})')

    # ---------------- E1 ----------------
    tieu_de('E1 · Chỉ số tính thử trên 1.200 yêu cầu (đợt chạy thử, không có đối chứng)')
    chinh = (reqs.dong_trong_24h == 1) & (reqs.mo_lai_trong_7_ngay == 0)
    xem = reqs[reqs.duoc_xem_lai == 1]
    bo_qua = xem.quyet_dinh_xem_lai.isin(['sua', 'bo'])
    an_toan = reqs.mo_lai_trong_7_ngay == 1
    print(f'Chính  : {chinh.mean() * 100:.2f}% ({chinh.sum()}/{len(reqs)})')
    print(f'Dùng   : {bo_qua.mean() * 100:.2f}% ({bo_qua.sum()}/{len(xem)}) bỏ qua gợi ý (sua + bo)')
    print(f'An toàn: {an_toan.mean() * 100:.2f}% ({an_toan.sum()}/{len(reqs)}) mở lại trong 7 ngày')
    print(f'Tỉ lệ được xem lại hiện tại: {reqs.duoc_xem_lai.mean() * 100:.1f}% ({len(xem)}/{len(reqs)})')
