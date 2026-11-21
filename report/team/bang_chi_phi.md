# Bảng chi phí · Nhiệm vụ A và B

Số tính bằng `src/lab13.py` (chạy `python lab13.py` trong `src/`). Mọi con số tính từ cột `_simulated` ghi nhãn `simulated`. Mỗi câu trả lời không quá ba dòng, có ít nhất một con số.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8)                              | Kết quả của nhóm                 |
| ----------------------------------------------- | -------------------------------- |
| Số lần chạy trung bình, tối đa 2 lần            | 1,20 · ĐẠT                       |
| Số lần chạy trung bình, chạy đến khi đúng       | 1,25 · ĐẠT                       |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 · ĐẠT (= 1/p, k triệt tiêu) |

## A2 · Mô hình chi phí từ trace

| Khoản                                     | Số tiền (đ) | Nguồn                                 | Nhãn              |
| ----------------------------------------- | ----------: | ------------------------------------- | ----------------- |
| Token                                     |     245.585 | `logix_runs.csv`                      | đo từ trace       |
| Tool                                      |      84.000 | `logix_runs.csv` (5.600 lần gọi)      | đo từ trace       |
| Trong đó, phần của lần chạy thứ 2 và 3    |      93.804 | attempt lớn hơn 1                     | đo từ trace       |
| Xem lại                                   |   1.780.000 | `phut_xem_lai_simulated` (890 phút)   | simulated         |
| Làm lại                                   |   2.264.000 | `phut_lam_lai_simulated` (1.132 phút) | simulated         |
| Tổng chi phí                              |   4.373.585 |                                       | có phần simulated |
| Số việc thành công                        |         978 | `ket_qua`                             |                   |
| Chi phí mỗi việc thành công               |       4.472 |                                       | simulated         |
| Hoá đơn token và tool chia cho số yêu cầu |       274,7 |                                       | đo từ trace       |

**Kiểm tay (người kiểm số):** token = 5.771.712 / 1.000 × 26 + 734.774 / 1.000 × 130 = 245.585 đ; CPS = 4.373.585 / 978 = 4.472 đ [simulated], khớp code.

- Chi phí mỗi việc thành công gấp **16,3 lần** hoá đơn chia số yêu cầu (4.472 / 274,7) [simulated]: thiếu giờ nhân viên thì sẽ chỉ thấy 1–2 lần.
- Khoản lớn nhất là **làm lại, 51,8%** tổng chi phí [simulated], tiếp theo là xem lại 40,7% [simulated]; giờ nhân viên chiếm 92,5% [simulated].
- So với nhân viên tự làm phải cộng 222 ca không thành công: (4.373.585 + 222 × 12.000) / 1.200 = **5.865 đ/yêu cầu = 0,49×** của 12.000 đ [simulated].

## A3 · Tách theo loại yêu cầu

| Loại      | Số yêu cầu | Tỉ lệ thành công | Số lần chạy mỗi yêu cầu | Chi phí mỗi việc thành công [simulated] | So với 12.000 đ |
| --------- | ---------: | ---------------: | ----------------------: | --------------------------------------: | --------------: |
| noi_dia   |        824 |            95,0% |                    1,11 |                                 2.696 đ |           0,22× |
| hang_nang |        158 |            74,1% |                    1,47 |                                 8.221 đ |           0,69× |
| quoc_te   |        150 |            27,3% |                    2,32 |                                22.515 đ |           1,88× |
| doi_tac   |         68 |            54,4% |                    1,88 |                                10.215 đ |           0,85× |

Tỉ lệ lần chạy `ok` theo attempt (đo từ trace): quoc_te 30,0% → 11,4% → 2,2%; doi_tac 51,5% → 18,2% → 14,8%; hang_nang 70,9% → 39,1% → 17,9%; noi_dia 91,0% → 75,7% → 38,9%.

- **quoc_te không đáng để trợ lý xử lý:** 1,88× của 12.000 đ [simulated], chỉ 27,3% thành công dù chạy 2,32 lần/yêu cầu.
- Chạy lại tới 3 lần không giúp: lần 2 chỉ đúng 11,4%, lần 3 còn 2,2%; lỗi lặp lại trên cùng yêu cầu nên chạy lại chỉ thêm tiền.
- doi_tac sát ngưỡng (0,85× [simulated], 54,4% thành công) và có điều khoản riêng, nên cũng loại khỏi phạm vi pilot.

## A4 · Chi phí cố định (phạm vi noi_dia + hang_nang)

Phạm vi: 982 yêu cầu, 900 thành công, tổng 3.072.513 đ → CPS 3.414 đ [simulated] trước khi cộng cố định.

| Khối lượng           |       Việc thành công mỗi tháng | Chi phí cố định mỗi việc | Chi phí mỗi việc thành công + cố định | So với 12.000 đ |
| -------------------- | ------------------------------: | -----------------------: | ------------------------------------: | --------------: |
| 45.000 yêu cầu/tháng | 33.750 (= 45.000 × 900 / 1.200) |                  1.185 đ |                   4.599 đ [simulated] |           0,38× |
| Một nửa khối lượng   |                          16.875 |                  2.370 đ |                   5.784 đ [simulated] |           0,48× |

- Chi phí cố định không đổi kết luận ở quy mô đầy đủ (0,38× [simulated]), nhưng khối lượng giảm một nửa thì cố định mỗi việc tăng gấp đôi lên 2.370 đ (0,48× [simulated]).
- Ở giai đoạn pilot (chỉ 50% nhân viên dùng trợ lý) phải báo con số đã cộng cố định theo khối lượng thực tế.

## B1 · Đổi từng yếu tố

| Kịch bản                   | Cách tính                                                                      | Chi phí mỗi việc thành công [simulated] | Thay đổi (%) |
| -------------------------- | ------------------------------------------------------------------------------ | --------------------------------------: | -----------: |
| Gốc (A2)                   |                                                                                |                                 4.472 đ |              |
| Giá token gấp đôi          | 52 đ và 260 đ cho 1.000 token; giá tool giữ nguyên                             |                                 4.723 đ |        +5,6% |
| Giá token giảm một nửa     | 13 đ và 65 đ                                                                   |                                 4.346 đ |        −2,8% |
| Tỉ lệ xem lại gấp đôi      | Tiền xem lại × 2                                                               |                                 6.292 đ |       +40,7% |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại ÷ 2                                                               |                                 3.562 đ |       −20,3% |
| Số ca làm lại gấp đôi      | Tiền làm lại × 2                                                               |                                 6.787 đ |       +51,8% |
| Số ca làm lại giảm một nửa | Tiền làm lại ÷ 2                                                               |                                 3.315 đ |       −25,9% |
| Lương nhân viên tăng 25%   | 2.500 đ mỗi phút                                                               |                                 5.506 đ |       +23,1% |
| Chỉ cho chạy tối đa 2 lần  | Bỏ lần chạy có attempt > 2; yêu cầu có so_lan_chay > 2 coi là chuyen_nhan_vien |                                 4.237 đ |        −5,2% |
| Chỉ cho chạy 1 lần         | Như trên với giới hạn 1                                                        |                                 4.111 đ |        −8,1% |

Tự kiểm tra: mỗi kịch bản "giảm một nửa" giảm đúng nửa mức tăng của "gấp đôi" (5,6 → 2,8; 40,7 → 20,3; 51,8 → 25,9).

## B2 · Đổi một cặp và xếp hạng

- Giá token gấp đôi cùng lúc tỉ lệ xem lại gấp đôi: **6.543 đ (+46,3%)** [simulated] = 5,6% + 40,7%, vì mô hình cộng tuyến tính.
- Xếp hạng ba yếu tố ảnh hưởng mạnh nhất: 1. **số ca làm lại** (±51,8%) · 2. **tỉ lệ xem lại** (±40,7%) · 3. **lương nhân viên** (+23,1% khi tăng 25%). Giá token chỉ ±5,6% [simulated].

## B3 · Giới hạn chạy lại có thật sự rẻ hơn

Chi phí cả hệ thống = tổng chi phí trợ lý + 12.000 đ × số yêu cầu không thành công (nhân viên làm thay).

| Giới hạn | Tổng chi phí trợ lý [simulated] | Số yêu cầu không thành công | Chi phí cả hệ thống [simulated] | Chi phí mỗi việc thành công [simulated] |
| -------- | ------------------------------: | --------------------------: | ------------------------------: | --------------------------------------: |
| 1 lần    |                     3.621.781 đ |                         319 |                     7.449.781 đ |                     4.111 đ (thấp nhất) |
| 2 lần    |                     4.093.220 đ |                         234 |       **6.901.220 đ (rẻ nhất)** |                                 4.237 đ |
| 3 lần    |                     4.373.585 đ |                         222 |                     7.037.585 đ |                                 4.472 đ |

- Giới hạn **2 lần rẻ nhất cho công ty** (6.901.220 đ [simulated]), **không trùng** với giới hạn có CPS thấp nhất (1 lần, 4.111 đ [simulated]).
- Tối ưu riêng CPS bằng giới hạn 1 lần đẩy thêm 85 việc (319 − 234) sang nhân viên, cả hệ thống đắt hơn 548.561 đ [simulated].

## B4 · Nếu phải xem lại tất cả

Phạm vi noi_dia + hang_nang (982 yêu cầu): 948 yêu cầu có ít nhất một lần chạy ok × 5 phút = 9.480.000 đ; 48 ca làm lại × 9 phút = 864.000 đ; token + tool 224.513 đ; tổng 10.568.513 đ ÷ 900 việc thành công.

- Xem lại 100%: **11.743 đ = 0,98×** của 12.000 đ [simulated]; nếu làm lại 15,3 phút/ca như dữ liệu (trung vị 14,5) thì **12.415 đ = 1,03×** [simulated], đắt hơn nhân viên tự làm.
- Tiền xem lại chiếm 90% tổng, nên trợ lý gần như không tiết kiệm; hoà vốn khi mỗi lần xem lại ≤ **5,1 phút** (làm lại 9 phút) hoặc ≤ **4,8 phút** (làm lại 15,3 phút) [simulated].
- Pilot phải học được: tỉ lệ xem lại giảm an toàn xuống mức nào (đợt chạy thử chỉ xem lại 14,8%) và mỗi lần xem lại có dưới 5 phút được không.
