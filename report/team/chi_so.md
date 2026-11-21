# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

Số tính bằng `src/lab13.py` trên 1.200 yêu cầu của đợt chạy thử (6 depot, 2 tuần, không có nhóm đối chứng).

## E1 · Đặc tả chỉ số

| Loại            | Chỉ số                                                                                       | Công thức                                                                                                        | Tính thử trên 1.200 yêu cầu                                            |
| --------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày                                     | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu                                    | **82,83%** (994/1.200)                                                 |
| Dùng            | Tỉ lệ bỏ qua gợi ý                                                                           | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại                                            | **27,12%** (48/177)                                                    |
| An toàn         | Tỉ lệ lỗi lọt đến khách                                                                      | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu                                                               | **4,25%** (51/1.200); trong phạm vi noi_dia + hang_nang 3,97% (39/982) |
| Dùng            | Nhóm tự đề xuất: % yêu cầu của NV nhóm trợ lý được mở bằng trợ lý                            | số `refund_request_created` có `agent_suggestion_shown` cùng `trace_id`, chia số yêu cầu giao cho NV nhóm trợ lý | Không cần tính                                                         |
| An toàn         | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần (bắt lỗi ngầm kiểu ca 5, 17) | số `audit_sample_checked` có `so_tien_da_hoan` khác `so_tien_dung`, chia số đơn được kiểm tra (100 đơn/tuần)     | Không cần tính                                                         |

Chỉ số trong đợt chạy thử là 82,83%. Không thể nói trợ lý đã nâng chỉ số so với mức 0,70 vì đợt chạy thử không có nhóm đối chứng; pilot 20 + 20 NV mới tách được tác động.

## Danh sách event

| Event                    | Ai tạo              | Thuộc tính chính                                                               | Thời điểm                       |
| ------------------------ | ------------------- | ------------------------------------------------------------------------------ | ------------------------------- |
| `refund_request_created` | App khách           | request_id, loai, so_tien, depot, staff_id, arm (tro_ly / doi_chung), trace_id | Khi khách gửi yêu cầu           |
| `agent_run_completed`    | Agent               | attempt, tokens_in, tokens_out, tool_calls, status, trace_id                   | Sau mỗi lần chạy, kể cả lần lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, trace_id                                            | Khi gợi ý hiện cho NV           |
| `staff_review_decision`  | Nhân viên           | quyet_dinh (giu / sua / bo), phut_xem_lai đo thật, trace_id                    | Khi NV bấm gửi, sửa hoặc bỏ     |
| `staff_rework_completed` | Nhân viên           | phut_lam_lai đo thật, ly_do, trace_id                                          | Khi làm lại xong                |
| `refund_ledger_write`    | Dịch vụ sổ cái      | idempotency_key, so_tien, ket_qua (ok / loi), trace_id                         | Khi ghi sổ hoàn tiền            |
| `handoff_to_staff`       | Agent               | reason (thieu_du_lieu, ngoai_pham_vi, het_lan_chay…), tom_tat, trace_id        | Khi chuyển cho nhân viên        |
| `ticket_closed`          | Hệ thống ticket     | closed_at, created_at, trace_id                                                | Khi đóng yêu cầu                |
| `ticket_reopened`        | Khách               | reopened_at, reason, trace_id                                                  | Khi khách mở lại                |
| `audit_sample_checked`   | Kế toán             | so_tien_da_hoan, so_tien_dung, phien_ban_bang_gia, trace_id                    | Hằng tuần, 100 đơn mẫu          |

**Kiểm tra chéo:**

- Chính: `refund_request_created` (mẫu số, arm) + `ticket_closed` (đóng trong 24 giờ) + `ticket_reopened` (mở lại trong 7 ngày).
- Dùng (bỏ qua gợi ý): `staff_review_decision` với quyet_dinh là sua hoặc bo, chia tổng số `staff_review_decision`.
- An toàn (lỗi lọt đến khách): `ticket_reopened` trong 7 ngày sau `ticket_closed`, chia `refund_request_created`.
- Dùng (tự đề xuất): `agent_suggestion_shown` nối `refund_request_created` qua `trace_id`.
- An toàn (tự đề xuất): `audit_sample_checked`.
- Chi phí mỗi việc thành công: `agent_run_completed` (token, tool) + `staff_review_decision` và `staff_rework_completed` (phút đo thật thay cho cột simulated).
- Hoàn trùng (luật dừng an toàn): hai `refund_ledger_write` ok cùng request_id.

## E2 · Rủi ro kinh tế

Số lấy từ bảng độ nhạy trong `bang_chi_phi.md`.

| Rủi ro                      | Tác động đã tính                                                                                                     | Dấu hiệu theo dõi                                                                                          | Hành động                                                             | Người phụ trách    |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------ |
| Số ca làm lại tăng gấp đôi  | +51,8%, chi phí mỗi việc thành công lên 6.787 đ [simulated]                                                          | Tỉ lệ `staff_rework_completed` theo tuần trên 7% (đợt chạy thử: 4,9% trong phạm vi, 48/982)                | Thu hẹp về noi_dia, rà 20 trace làm lại gần nhất                      | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài   | 11.743 đ = 0,98× (12.415 đ = 1,03× nếu làm lại 15,3 phút như dữ liệu) [simulated]                                    | % yêu cầu có `staff_review_decision` còn trên 50% cuối bước rollout 0.25, hoặc phút xem lại TB trên 5 phút | Giảm xem lại theo bậc khi tỉ lệ sua + bo dưới 15%                     | Trưởng nhóm CSKH   |
| Khối lượng thấp hơn dự kiến | Cố định 40 triệu/tháng: +1.185 đ/việc ở 45.000 yc/tháng, +2.370 đ/việc nếu còn một nửa (5.784 đ = 0,48×) [simulated] | Số việc thành công theo tuần dưới 50% kế hoạch                                                             | Không mở rộng pilot, xem lại hợp đồng chi phí cố định                 | PM trợ lý hoàn phí |
| Lương nhân viên tăng 25%    | +23,1%, lên 5.506 đ [simulated]                                                                                      | Đơn giá phút NV do phòng nhân sự cập nhật mỗi quý                                                          | Cập nhật mô hình chi phí, kiểm tra lại ngưỡng 8.000 đ trong luật dừng | Kế toán trưởng     |
