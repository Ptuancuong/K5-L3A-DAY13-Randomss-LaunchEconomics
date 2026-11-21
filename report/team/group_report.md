# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: Randomss (nhóm 1 thành viên: Phạm Tuấn Cường, 2A202603584)
- Lớp: L3A
- Thành viên: xem `TEAM.md`

## 2. Mục tiêu và cách tiếp cận

Dựng hồ sơ launch v0 cho trợ lý hoàn phí LogiX-VN để Gate 2a duyệt **kế hoạch pilot**, trả lời bốn câu: có đáng chạy không, nhân viên có dùng không, khi hỏng thì sao, pilot thiết kế thế nào để ra được quyết định. Mọi con số do `src/lab13.py` tính từ hai file CSV (dữ liệu giả lập), đối chiếu với slide chữa sau mỗi checkpoint; số tính từ cột `_simulated` ghi nhãn `simulated`.

## 3. Giải pháp

| Nhiệm vụ                        | Cách làm                                                                                                                                                                                         | File                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| A · Chi phí mỗi việc thành công | Ba hàm A1 (qua 1,20 · 1,25 · 1,25); `mo_hinh` cộng token + tool của mọi lần chạy, kể cả lần lỗi, cộng phút xem lại và làm lại, chia cho số việc thành công; tách theo loại; cộng chi phí cố định | [bang_chi_phi.md](bang_chi_phi.md), [lab13.py](../../src/lab13.py) |
| B · Độ nhạy                     | 9 kịch bản đổi một yếu tố, một cặp, giới hạn 1/2/3 lần chạy tính cả hệ thống, xem lại 100%                                                                                                       | [bang_chi_phi.md](bang_chi_phi.md)                                 |
| C · Bảng lỗi                    | Hai lượt gắn nhãn 20 ca theo năm loại Google PAIR, so nhãn, thống nhất, bảng khắc phục 5 ca                                                                                                      | [bang_loi.md](bang_loi.md)                                         |
| D · Pilot                       | Tính năm câu D1 trước, chọn chia theo nhân viên 20 + 20, chấp nhận MDE 6 điểm, đặt luật dừng sau khi xem tỉ lệ mở lại hiện tại                                                                   | [pilot_plan.yaml](pilot_plan.yaml)                                 |
| E · Chỉ số, rủi ro, hồ sơ       | Tính thử ba chỉ số, 10 event có `trace_id`, 4 dòng rủi ro lấy số từ B, hồ sơ một trang bảy mục                                                                                                   | [chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)   |

## 4. Kết quả

- Chi phí mỗi việc thành công **4.472 đ** [simulated], gấp **16,3×** hoá đơn token + tool chia số yêu cầu (274,7 đ); làm lại chiếm 51,8% [simulated]. Cả hệ thống 5.865 đ/yêu cầu = 0,49× của 12.000 đ [simulated].
- Theo loại: noi_dia 0,22×, hang_nang 0,69×, quoc_te 1,88×, doi_tac 0,85× [simulated] → phạm vi pilot chỉ noi_dia + hang_nang (3.414 đ, cộng cố định 4.599 đ = 0,38× [simulated]).
- Ba yếu tố nhạy nhất: số ca làm lại (±51,8%), tỉ lệ xem lại (±40,7%), lương NV (+23,1%) [simulated]. Giới hạn 2 lần chạy rẻ nhất cho công ty (6.901.220 đ [simulated]). Xem lại 100% còn 0,98×–1,03× [simulated].
- Bảng lỗi: đồng thuận 18/20 = 90% giữa hai lượt gắn nhãn.
- Pilot: chia theo NV 20 + 20, MDE 6 điểm, 859 mỗi nhóm, DE 6,96, mỗi NV ≥ 299 yêu cầu; power chỉ 0,64 nếu tác động thật 5 điểm. Chỉ số trong đợt chạy thử: chính 82,83%, bỏ qua gợi ý 27,12%, mở lại 7 ngày 4,25%.
- **Đề xuất của hồ sơ: Go có điều kiện** cho pilot noi_dia + hang_nang (sửa khoá chống trùng và đối soát sổ cái, ký chấp nhận MDE 6 điểm, bật đủ event, kế hoạch giảm xem lại theo bậc).
- Kết quả duyệt chéo nhóm nhận được từ hội đồng: ... (nhóm hội đồng: ..., điểm ... / 30, quyết định ...).

## 5. Khó khăn và cách xử lý

- **Nhóm chỉ có 1 thành viên:** một người giữ cả bốn vai. Vai "người kiểm số" thay bằng tính tay token (245.585 đ) và CPS (4.373.585 / 978 = 4.472 đ) để đối chiếu với code.
- **Nhiệm vụ C cần hai bộ nhãn độc lập:** không có người gắn nhãn thứ hai nên gắn hai lượt cách nhau 30 phút, lượt 2 che cột lượt 1, mỗi lượt 8 phút; đồng thuận 18/20, hai ca lệch (13, 20) thống nhất bằng quy tắc nguyên nhân gốc trong `bang_loi.md`. Hai lượt do cùng một người gắn nên chưa độc lập thật sự; tỉ lệ 90% có thể cao hơn so với hai người khác nhau.
- **Môi trường Windows:** dùng `py -3 -m venv` và `.\.venv\Scripts\Activate.ps1`; thêm `sys.stdout.reconfigure(encoding='utf-8')` để console in đúng tiếng Việt.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Phút xem lại và làm lại là số giả lập; pilot phải thay bằng phút đo thật từ `staff_review_decision`, `staff_rework_completed` sau tuần 1.
- Với 40 NV, pilot không đủ mẫu để thấy mức chênh 5 điểm (tối đa 1.000 < 1.251); nếu tác động thật chỉ 5 điểm, khả năng bỏ sót là khoảng 36%.
- Đợt chạy thử không có đối chứng, nên 82,83% chỉ là chỉ số trong đợt chạy thử, chưa nói được tác động của trợ lý.
- Hai bộ nhãn C do cùng một người gắn; cần một người thứ hai gắn độc lập để kiểm tra định nghĩa.

## 8. Tài liệu tham khảo

- Erol và cộng sự, _Cost-of-Pass: An Economic Framework for Evaluating Language Models_, arxiv.org/abs/2504.13359
- Google PAIR, _People + AI Guidebook_, chương "Errors + Graceful Failure"
- Tài liệu statsmodels, `NormalIndPower`, `proportion_effectsize`
- `docs/du_lieu_va_cong_thuc.md`, `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`
