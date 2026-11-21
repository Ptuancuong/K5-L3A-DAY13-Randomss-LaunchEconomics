# Plan Lab 13 · Launch Economics (nhóm 1 người)

Repo: `K5-L3A-DAY13-Randomss-LaunchEconomics` · Lớp L3A · Deadline nộp: **23h59 GMT+7 ngày lab** (hồ sơ phải có đủ 7 mục lúc **17:00** để duyệt chéo).

## 0. Điều chỉnh vì nhóm chỉ có 1 người

| Vấn đề                                                              | Cách xử lý                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bốn vai (viết code, kiểm số, gắn nhãn 1, gắn nhãn 2 kiêm giữ hồ sơ) | Một mình đảm nhận cả bốn; ghi rõ trong `TEAM.md` và báo cáo cá nhân                                                                                                                                                                                                  |
| "Người kiểm số"                                                     | Tự tính tay ít nhất 1 con số (ví dụ CPS = 4.373.585 / 978) và ghi cách tính vào `bang_chi_phi.md`                                                                                                                                                                    |
| Nhiệm vụ C cần **hai bộ nhãn độc lập**                              | Phương án dự phòng: tự gắn 2 lượt cách nhau ≥ 30 phút, lượt 2 xáo thứ tự ca, không xem lượt 1; ghi trung thực cách làm trong `bang_loi.md` và mục 5 `group_report.md` |
| Không đọc trước đáp án C                                            | Mục "Nhãn tham khảo cho 20 ca" trong `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md` có đáp án → **không mở mục đó trước khi gắn xong cả hai lượt**                                                                                                                    |
| Duyệt chéo Gate 2a                                                  | Vẫn phải chấm một nhóm khác (nhóm n + 1) và được một nhóm chấm. Hỏi coach số thứ tự nhóm                                                                                                                                                                             |
| Ít người, nhiều việc                                                | Ưu tiên theo điểm: A (20) → B (15) → D (15) → C (10) → E (10). Hồ sơ v0 điền dần sau mỗi CP, không đợi tới 16:36                                                                                                                                                     |

## 1. Chuẩn bị (14:00–14:10)

- [ ] Điền `TEAM.md`: tên nhóm `Randomss`, lớp L3A, 1 thành viên giữ cả 4 vai.
- [ ] Copy `report/team/MSSV_HoTen.md` → `report/team/<MSSV>_PhamTuanCuong.md` (giữ file mẫu).
- [ ] Cài môi trường (PowerShell, trong `src/`):

```powershell
cd src
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "import pandas, numpy, scipy, statsmodels; print('san sang')"
```

- [ ] Hỏi coach: (1) cách gắn nhãn C khi làm 1 mình, (2) số thứ tự nhóm để biết chấm ai.

## 2. CP1 · Nhiệm vụ A · Chi phí mỗi việc thành công (14:10–14:53) · 20 điểm

File: `src/lab13.py`, `report/team/bang_chi_phi.md`

- [ ] **A1**: viết `so_lan_chay_ky_vong`, `ti_le_thanh_cong`, `he_so_chi_phi_moi_viec_thanh_cong` → chạy `python lab13.py` phải in `ĐẠT` (1,20 · 1,25 · 1,25). **Chưa đạt thì không làm tiếp.**
- [ ] **A2**: viết `mo_hinh(...)` trả về `token, tool, chay_lai, xem_lai, lam_lai, tong, thanh_cong, cps, hoa_don_moi_yc`.
  - Tử số tính **mọi** lần chạy (kể cả lỗi); mẫu số chỉ đếm `ket_qua == 'thanh_cong'`.
  - Chia 1.000 trước khi nhân giá token; đọc CSV với `keep_default_na=False`.
  - Hỗ trợ sẵn `max_lan_chay` (dùng cho B).
- [ ] **A3**: lặp `mo_hinh(runs, reqs[reqs.loai == l])` cho 4 loại; thêm pivot tỉ lệ `ok` theo `attempt` × `loai` để trả lời "chạy lại có giúp không".
- [ ] **A4**: chi phí cố định 40 tr/tháng cho phạm vi `noi_dia` + `hang_nang` ở 45.000 yc/tháng và một nửa khối lượng.
- [ ] Điền bảng A1–A4, 2 dòng xem lại/làm lại ghi nhãn **simulated**; tự tính tay 1 số.
- [ ] Commit: `CP1: mo hinh chi phi A1-A4`.

**Số để tự đối chiếu (lệch ≤ 2%):** token 245.585 · tool 84.000 · lần 2–3: 93.804 · xem lại 1.780.000 [sim] · làm lại 2.264.000 [sim] · tổng 4.373.585 · thành công 978 · CPS 4.472 đ [sim] · hoá đơn/yc 274,7 → gấp 16,3×; làm lại lớn nhất 51,8% [sim].
A3: noi_dia 2.696 (0,22×) · hang_nang 8.221 (0,69×) · quoc_te 22.515 (1,88×) · doi_tac 10.215 (0,85×).
A4: 33.750 việc/tháng → +1.185 đ → 4.599 đ (0,38×); nửa khối lượng → 5.784 đ (0,48×).

## 3. CP2 · Nhiệm vụ B · Bảng độ nhạy (14:53–15:20) · 15 điểm

File: `src/lab13.py` (dòng `TODO CP2`), `report/team/bang_chi_phi.md`

- [ ] **B1**: dict 9 kịch bản, mỗi kịch bản gọi `mo_hinh` với 1 tham số đổi, in CPS và % thay đổi.
- [ ] **B2**: cặp giá token ×2 + xem lại ×2; xếp hạng 3 yếu tố.
- [ ] **B3**: giới hạn 1/2/3 lần chạy → tổng trợ lý, số không thành công, chi phí cả hệ thống (+12.000 đ × số không thành công), CPS.
- [ ] **B4**: xem lại 100% cho `noi_dia` + `hang_nang` (5 phút/yc có ≥1 lần ok, 9 phút/ca làm lại) + độ nhạy với 15,3 phút làm lại + mức hoà vốn.
- [ ] Mỗi câu trả lời ≤ 3 dòng, có số, nhãn simulated.
- [ ] Commit: `CP2: bang do nhay B1-B4`.

**Đối chiếu:** token ×2 4.723 (+5,6%) · ÷2 4.346 (−2,8%) · xem lại ×2 6.292 (+40,7%) · ÷2 3.562 (−20,3%) · làm lại ×2 6.787 (+51,8%) · ÷2 3.315 (−25,9%) · lương +25% 5.506 (+23,1%) · tối đa 2 lần 4.237 (−5,2%) · 1 lần 4.111 (−8,1%).
B2: 6.543 đ (+46,3%) = tổng hai tác động · Xếp hạng: làm lại > xem lại > lương.
B3: 2 lần rẻ nhất cho công ty (6.901.220 đ) ≠ 1 lần có CPS thấp nhất (4.111 đ).
B4: 11.743 đ = 0,98× (12.414 đ = 1,03× nếu làm lại 15,3 phút); hoà vốn ≤ 5,1 / 4,8 phút xem lại.

**Giải lao 15:20–15:35:** dùng 10 phút điền mục 1–3 của `ho_so_launch_v0.md` bằng số A, B.

## 4. CP3 · Nhiệm vụ C · Bảng lỗi (15:35–16:08) · 10 điểm

File: `report/team/bang_loi.md` · 20 ca lấy từ `docs/Ngay13_Lab13_De_bai_hoc_vien.docx` (mục "Hai mươi ca lỗi")

- [ ] Nắm 5 loại PAIR: Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm. **Gắn theo nguyên nhân gốc, không theo chỗ cần sửa.**
- [ ] **Bộ nhãn 1** (8 phút): tự gắn 20 ca, lưu ngay vào file, không sửa sau.
- [ ] **Bộ nhãn 2**: theo phương án coach đồng ý (bạn nhóm khác, hoặc tự gắn lượt 2 sau ≥ 30 phút — có thể làm lượt 2 sau CP4).
- [ ] So nhãn, tính đồng thuận (mục tiêu ≥ 16/20); mỗi ca lệch ghi 1 câu quy tắc phân biệt. Dưới 80% → viết lại định nghĩa.
- [ ] Bảng khắc phục 5 ca (mỗi loại 1 ca): cách phát hiện **đo được** (event + ngưỡng + tần suất), 1 vai trò phụ trách (PM trợ lý hoàn phí, Kỹ sư trưởng agent, Trưởng nhóm CSKH, Kế toán trưởng…). Không ghi "cả đội".
- [ ] Chỉ sau khi xong hai bộ nhãn mới đối chiếu slide chữa / bảng tham khảo; **không sửa bộ nhãn độc lập**, chỉ sửa cột "Nhãn thống nhất".
- [ ] Commit: `CP3: bang loi`.

Mẹo phân biệt: lỗi đã lộ ra (có người thấy) → Hệ thống; không ai thấy tới khi kiểm tra mẫu → Ngầm; đúng chính sách nhưng giả định lệch hoàn cảnh khách → Ngữ cảnh; ngoài phạm vi/không có dữ liệu → Giới hạn, kể cả khi xử lý giới hạn đó kém.

## 5. CP4 · Nhiệm vụ D · pilot_plan.yaml (16:08–16:36) · 15 điểm

File: `src/lab13.py` (dòng `TODO CP4`), `report/team/pilot_plan.yaml`

- [ ] **D1** trong code (hàm `co_mau` + DE + n hiệu dụng), in 5 câu:
  - a) theo yêu cầu: **1.251**/nhóm
  - b) theo nhân viên m = 75: DE 2,48 → 3.103/nhóm → 42 người/nhóm, cần 84 > 40 → không đủ người
  - c) 20 NV/nhóm: tối đa 20/0,02 = **1.000** < 1.251 → không đạt
  - d) 6 depot/nhóm: tối đa **300**
  - e) chênh 6 điểm (859/nhóm), 20 NV/nhóm: m ≥ **299** yc/người (DE 6,96)
  - thêm: power chỉ ~0,64 nếu tác động thật là 5 điểm (`NormalIndPower`) → con số bất lợi phải nêu.
- [ ] Tính `mo_lai_trong_7_ngay` hiện tại: 4,25% (toàn bộ), 3,97% (noi_dia + hang_nang) → **không đặt ngưỡng tuyệt đối 3%**; dùng so với đối chứng (+2 điểm) kèm trần 6%.
- [ ] Chọn cách chia: **theo nhân viên, 20 + 20, ngẫu nhiên có seed, phân tầng theo depot**, chấp nhận MDE 0,06.
- [ ] D2: trả lời 5 câu "tách được tác động" vào phần chú thích đầu file.
- [ ] Điền mọi trường: `owner` (Giám đốc vận hành), `scope` (noi_dia + hang_nang, lý do bằng số A3), `assignment.unit: staff`, `mde: 0.06`, `n_per_arm: 859`, `design_effect: 6.96`, `clusters_per_arm: 20`, `identifiability.*`, ≥ 3 `stop_rules` (an toàn, chi phí, mức dùng) đủ 4 vế **NẾU – TRONG – THÌ – KHÔNG THÌ**, `rollback`, `decision_date`, `simulated_inputs`.
- [ ] Kiểm tra (trong `src/`):

```powershell
python -c "import yaml; yaml.safe_load(open('../report/team/pilot_plan.yaml', encoding='utf-8'))"
Select-String -Path ../report/team/pilot_plan.yaml -Pattern '^\s*#' -NotMatch | Select-String -Pattern '\?'
```

Lệnh 2 không được in dòng nào.

- [ ] Commit: `CP4: pilot plan`.

## 6. CP5 · Nhiệm vụ E · Chỉ số, rủi ro, hồ sơ v0 (16:36–17:00) · 10 điểm

File: `report/team/chi_so.md`, `report/team/ho_so_launch_v0.md`

- [ ] **E1** tính thử (thêm vào `lab13.py`): chính 82,83% (994/1.200) · dùng (bỏ qua gợi ý) 27,12% (48/177) · an toàn (mở lại 7 ngày) 4,25% (51/1.200). Viết "chỉ số trong đợt chạy thử là…", không viết "trợ lý đã nâng…".
- [ ] Đề xuất thêm 1 chỉ số dùng + 1 chỉ số an toàn (ví dụ: kiểm tra mẫu hằng tuần bắt lỗi ngầm như ca 5, 17).
- [ ] ≥ 6 event, mỗi event có `trace_id` (refund_request_created, agent_run_completed, agent_suggestion_shown, staff_review_decision, staff_rework_completed, refund_ledger_write, handoff_to_staff, ticket_closed, ticket_reopened…); kiểm tra chéo mỗi chỉ số ↔ event.
- [ ] **E2** ≥ 2 dòng rủi ro kinh tế lấy số từ B (làm lại ×2: +51,8% → 6.787 đ [sim]; xem lại 100%: 0,98×–1,03× [sim]; khối lượng thấp: +1.185 → +2.370 đ/việc).
- [ ] **E3** hồ sơ v0: 7 mục, mỗi mục có con số chính, trạng thái (**Xong, có bằng chứng · Chưa · Giả lập** — mục 1, 2, 3, 7 là Giả lập), 1 vai trò phụ trách.
- [ ] Dòng cuối: **Go có điều kiện** cho pilot noi_dia + hang_nang (chỉ chọn nếu số của mình khớp), mỗi điều kiện có người phụ trách + ngày kiểm tra; nêu rõ con số bất lợi (power 0,64, xem lại 100% ≈ 0,98×, chưa tính 148 ca chuyển nhân viên → so sánh đúng là 0,49×).
- [ ] Kiểm tra từ cấm (quy tắc 5 README) trong `report/team`:

```powershell
Select-String -Path ../report/team/* -Pattern 'production'
```

- [ ] Commit + push: `CP5: chi so, ho so launch v0` — **bản này phải có trước 17:00**.

## 7. Duyệt chéo Gate 2a (17:00–17:45) · 30 điểm do hội đồng chấm

- [ ] 17:00 gửi link `ho_so_launch_v0.md` cho nhóm hội đồng.
- [ ] 17:10 đọc hồ sơ nhóm n + 1, chấm 3 tiêu chí (0/5/10, lý do có số) vào `report/team/phieu_cham.md`, ghi quyết định + 1 câu hỏi (ví dụ: "CPS là bao nhiêu nếu tuần đầu xem lại 100%?", "cách chia có ≥ 20 cụm mỗi nhóm không?").
- [ ] 17:25 trình 1 phút, chuẩn bị sẵn câu trả lời cho 3 câu hỏi gợi ý của đề; ghi câu trả lời của đội kia vào phiếu.
- [ ] Ghi kết quả nhóm mình nhận được để đưa vào `group_report.md`.

## 8. Đóng gói và nộp (17:45 → trước 23h59)

- [ ] `group_report.md` (≤ 2 trang): mục tiêu, cách làm A–E, số chính, đề xuất, kết quả duyệt chéo, khó khăn (làm 1 mình, cách gắn nhãn C).
- [ ] Báo cáo cá nhân: vai, đóng góp, bằng chứng (commit), công cụ AI đã dùng và cách tự kiểm tra.
- [ ] `TEAM.md`: URL repo, nhánh `main`, commit chốt.
- [ ] Chạy lại từ đầu trong môi trường sạch: `python lab13.py` in đủ A1 ĐẠT, A2, A3, B, D1.
- [ ] Rà checklist `SUBMISSION.md`: đủ 6 file hồ sơ đúng tên, nhãn simulated, YAML hợp lệ, không `?`, không từ cấm, không `.venv/` / `.env`.
- [ ] Push lên GitHub, repo public (hoặc mời giảng viên), **nộp link repo trên LMS bằng tài khoản cá nhân**.
- [ ] Sửa sau deadline chỉ bằng commit mới, không force-push.

## 9. Những điều phải tự giải thích được khi bị hỏi

1. Vì sao tử số tính mọi lần chạy còn mẫu số chỉ đếm việc thành công.
2. Vì sao quoc_te không đáng chạy và chạy lại không giúp (ok theo lần: 30% → 11,4% → 2,2%).
3. Vì sao giới hạn rẻ nhất cho công ty (2 lần) khác giới hạn có CPS thấp nhất (1 lần).
4. Hệ số thiết kế, cỡ mẫu hiệu dụng < c / ICC; vì sao số cụm quyết định chứ không phải tổng số yêu cầu.
5. Lý do của đề xuất cuối, kèm con số bất lợi và cách xử lý.
