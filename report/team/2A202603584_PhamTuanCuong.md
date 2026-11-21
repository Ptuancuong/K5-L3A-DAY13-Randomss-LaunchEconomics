# Báo cáo cá nhân — PhamTuanCuong-2A202603584

## 1. Thông tin thành viên

- Họ tên: Phạm Tuấn Cường
- MSSV: 2A202603584
- Email: ...
- Vai trong nhóm: nhóm 1 thành viên, đảm nhận cả bốn vai (người viết code, người kiểm số, người gắn nhãn 1, người gắn nhãn 2 kiêm giữ hồ sơ)

## 2. Phần việc phụ trách

Toàn bộ nhiệm vụ A–E, duyệt chéo Gate 2a (chấm nhóm khác và trình bày hồ sơ của nhóm), đóng gói và nộp bài.

## 3. Đóng góp cụ thể

- **A, B:** viết ba hàm A1, hàm `mo_hinh`, tách theo loại (A3), cộng chi phí cố định (A4), chín kịch bản độ nhạy, một cặp, giới hạn lần chạy và xem lại 100% (B1–B4) trong `src/lab13.py`; điền `bang_chi_phi.md`.
- **C:** gắn hai bộ nhãn 20 ca, tính đồng thuận, viết bảng khắc phục 5 ca trong `bang_loi.md`.
- **D:** tính năm câu D1, chọn cách chia theo nhân viên 20 + 20 với MDE 6 điểm, viết `pilot_plan.yaml` với bốn luật dừng.
- **E:** tính thử ba chỉ số, liệt kê 10 event có `trace_id`, bốn dòng rủi ro kinh tế (`chi_so.md`), hồ sơ `ho_so_launch_v0.md`.

## 4. Bằng chứng

- `python lab13.py` in: A1 ĐẠT (1,20 · 1,25 · 1,25); CPS 4.472 đ [simulated], gấp 16,3× hoá đơn; B1 đủ 9 dòng; D1 1.251 / 3.103 / 1.000 / 300 / 299; E1 82,83% · 27,12% · 4,25%.
- Kiểm tay: token = 5.771.712 / 1.000 × 26 + 734.774 / 1.000 × 130 = 245.585 đ; CPS = 4.373.585 / 978 = 4.472 đ.
- Commit trên nhánh `main` của repo `K5-L3A-DAY13-Randomss-LaunchEconomics`.

## 5. Công cụ AI đã dùng

- Claude Code: lập kế hoạch làm bài (`plan.md`), gợi ý code cho `lab13.py` và soạn nháp các file hồ sơ từ output của code.
- Cách tự kiểm tra: chạy `python lab13.py` và đối chiếu từng con số với bảng số trong `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md` và slide chữa (lệch ≤ 2%); tính tay token và CPS; kiểm tra `pilot_plan.yaml` bằng `yaml.safe_load` và không còn dấu `?`.
- Không dùng AI để gắn nhãn 20 ca lỗi ở nhiệm vụ C: hai bộ nhãn do tôi tự gắn.

## 6. Tự đánh giá

...
