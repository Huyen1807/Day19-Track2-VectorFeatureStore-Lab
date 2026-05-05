# Reflection — Lab 19

**Tên:** Nguyễn Thị Thanh Huyền
**Cohort:** A20-K1
**Path đã chạy:** lite


## Câu hỏi (≤ 200 chữ)
Lab này cho mình 3 insight chính:

**1. Embedding làm cầu nối giữa text và vector:** Dùng fastembed, cùng một câu query được biến thành 384-dim vector. Paraphrase query (không chứa từ khóa gốc) vẫn trả về đúng topic cluster — chứng tỏ semantic embedding nắm bắt ý nghĩa, không chỉ keyword matching.

**2. Hybrid search hơn đơn lẻ:** BM25 nhanh, semantic tổng quát, RRF kết hợp cả hai. Trên data corpus VN, hybrid thắng trung bình so với kw/sem riêng lẻ, đặc biệt slice `mixed` query.

**3. Feast materialize + online lookup:** Feature store không chỉ offline; PIT join tránh data leakage, materialization nạp dữ liệu sang online store để lookup < 10ms (lý tưởng) hoặc chịu tradeoff performance vs consistency.

Challenge: SQLite trên Windows cho P99 ~25-30ms, vượt rubric. Docker+Redis là giải pháp thực tế cho latency ổn định.

> Trên golden set 50 queries, mode nào thắng ở loại query nào (`exact` /
> `paraphrase` / `mixed`), và tại sao? Khi nào bạn **không** dùng hybrid
> (i.e. khi nào pure BM25 hoặc pure vector là lựa chọn đúng)?

Trên golden set 50 queries mình quan sát được pattern điển hình:

- `exact`: **BM25** thường thắng vì queries dạng exact cần khớp từ vựng chính xác — BM25 khai thác TF/IDF và trả về những tài liệu có overlap từ khóa cao.
- `paraphrase`: **vector (semantic)** thắng vì embedding nắm được ý nghĩa, không phụ thuộc vào surface form; các paraphrase trả về kết quả đúng chủ đề dù không có từ khóa trùng.
- `mixed`: **hybrid (RRF)** thắng tổng thể — RRF kết hợp ưu điểm BM25 (precision với exact) và vector (recall cho paraphrase), thường cho top-k cân bằng hơn.

Khi **không** dùng hybrid:
- Nếu hệ thống yêu cầu latency cực thấp hoặc môi trường tài nguyên hạn chế (ví dụ realtime strict, edge device), có thể chọn **pure BM25** vì triển khai và truy vấn rất nhẹ.
- Nếu dữ liệu/ứng dụng chủ yếu cần hiểu intent/semantic (ví dụ paraphrase-heavy recommendation) và bạn có vector index nhanh (Redis/FAISS), **pure vector** là lựa chọn hợp lý.

Tóm lại, chọn hybrid khi bạn muốn cân bằng precision + recall; chọn một phương pháp nguyên chất khi constraint về latency, tài nguyên, hoặc tính chất truy vấn làm phương pháp đó rõ ràng vượt trội.

---

## Điều ngạc nhiên nhất khi làm lab này

_(Optional, 1–2 câu)_

---

## Bonus challenge

- [ ] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: _<tên đồng đội nếu có>_
