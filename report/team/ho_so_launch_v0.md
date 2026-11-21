# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: Randomss (1 thành viên: Phạm Tuấn Cường) · Lớp: L3A

| Mục                                           | Con số chính                                                                                                                                                                                                                    | Trạng thái          | Người phụ trách    |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------ |
| 1 · Chi phí mỗi việc thành công               | 4.472 đ/việc [simulated], gấp 16,3× hoá đơn token + tool chia số yêu cầu (274,7 đ); làm lại chiếm 51,8% [simulated]. Phạm vi noi_dia + hang_nang: 3.414 đ, cộng cố định 4.599 đ [simulated]                                     | Giả lập             | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất                       | 1. Số ca làm lại ±51,8% · 2. Tỉ lệ xem lại ±40,7% · 3. Lương NV +23,1%; giá token chỉ ±5,6% [simulated]                                                                                                                         | Giả lập             | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm                   | Cả hệ thống 5.865 đ/yêu cầu = 0,49× của 12.000 đ (đã cộng 222 ca không thành công) [simulated]; noi_dia 0,22×, hang_nang 0,69×, quoc_te 1,88×, doi_tac 0,85× [simulated]; **bất lợi:** xem lại 100% thì 0,98×–1,03× [simulated] | Giả lập             | Giám đốc vận hành  |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Chỉ số trong đợt chạy thử: chính 82,83% (994/1.200) · bỏ qua gợi ý 27,12% (48/177) · mở lại 7 ngày 4,25% (51/1.200); 10 event có trace_id                                                                                       | Xong, có bằng chứng | Trưởng nhóm CSKH   |
| 5 · Bảng lỗi và cách khắc phục | Hai bộ nhãn 20 ca, đồng thuận 18/20 = 90% (lệch ca 13, 20); bảng khắc phục 5 ca, mỗi loại 1 ca: ca 1, 7, 16, 13, 17 (`bang_loi.md`) | Xong, có bằng chứng | Kỹ sư trưởng agent |
| 6 · Pilot plan                                | Chia theo NV 20 + 20, ngẫu nhiên phân tầng theo depot; MDE 6 điểm, 859/nhóm, DE 6,96, ≥ 299 yc/NV; **bất lợi:** power 0,64 nếu tác động thật 5 điểm; 4 luật dừng NẾU–TRONG–THÌ–KHÔNG THÌ; quyết định 2027-01-29                 | Xong, có bằng chứng | Giám đốc vận hành  |
| 7 · Rủi ro kinh tế                            | Làm lại ×2: 6.787 đ (+51,8%) · xem lại 100%: 0,98×–1,03× · nửa khối lượng: +2.370 đ/việc cố định (0,48×) · lương +25%: 5.506 đ [simulated]                                                                                      | Giả lập             | PM trợ lý hoàn phí |

Phạm vi thu hẹp có lý do bằng số: chỉ noi_dia + hang_nang (982/1.200 yêu cầu, 900 thành công); loại quoc_te (1,88× [simulated], thành công 27,3%, lần chạy 2 và 3 chỉ đúng 11,4% và 2,2%) và doi_tac (0,85× [simulated], điều khoản riêng).

**Đề xuất: Go có điều kiện** cho pilot noi_dia + hang_nang, 20 + 20 NV, bắt đầu 2026-12-01.

- Sửa khoá chống trùng khi hoàn tiền (ca 20) và chỉ báo "đã hoàn" khi sổ cái trả ok (ca 7); kiểm thử 0 ca hoàn trùng. Phụ trách: Kỹ sư trưởng agent · kiểm tra 2026-11-28.
- Giám đốc vận hành ký chấp nhận MDE 6 điểm (power chỉ 0,64 nếu tác động thật 5 điểm) và mỗi NV nhóm trợ lý xử lý ≥ 299 yêu cầu. Phụ trách: Giám đốc vận hành · kiểm tra 2026-11-30.
- Bật đủ 10 event có trace_id; thay phút simulated bằng phút đo thật từ `staff_review_decision`, `staff_rework_completed` sau tuần 1. Phụ trách: PM trợ lý hoàn phí · kiểm tra 2026-12-08.
- Có kế hoạch giảm xem lại theo bậc, vì xem lại 100% chỉ còn 0,98×–1,03× [simulated] (B4); thời gian xem lại TB phải ≤ 5 phút. Phụ trách: Trưởng nhóm CSKH · kiểm tra 2026-12-15.
