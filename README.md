Họ và tên: Lù Đình Hưng

Lớp: K59.KMT.K01

GV: Đỗ Duy Cốp

## Môn học: An toàn thông tin



### 1. Tìm hiểu thuật toán mã hoá hiện đại DES, AES mô tả đc thuật toán, quy trình mã hoá/giải mã cài đặt AES trên 1 ngôn ngữ lập trình nào đó

## 1.0 Đối xứng nghĩa là gì?

"Đối xứng" nghĩa là **cùng một chiếc chìa** dùng cho cả hai việc: khóa lại và mở ra.

```
Lan:   [Bản rõ] ──khóa bằng K──► [Bản mã] ═══ đường truyền ═══► 
Minh:                                             [Bản mã] ──mở bằng K──► [Bản rõ]
```

Ưu điểm lớn nhất là **tốc độ**. Nhược điểm cũng rõ ràng: trước khi nói chuyện, Lan và Minh phải bằng cách nào đó đưa được chiếc chìa K cho nhau mà Tùng không nhìn thấy. Hãy nhớ nhược điểm này, vì Chặng 2 sinh ra để giải quyết nó.

DES và AES đều là **mã khối**: cắt dữ liệu thành từng khối cỡ cố định rồi xử lý từng khối một.

---

## 1.1 DES

### Hình dung

Cầm 64 lá bài (64 bit), chia thành hai xấp: **tay trái 32 lá** và **tay phải 32 lá**. Sau đó lặp lại 16 lượt cùng một động tác. Đây là mô hình **Feistel**.

### Một lượt xáo diễn ra thế nào?

```
   Trái (L)              Phải (R)
      │                     │
      │                ┌────┴─────┐
      │                │  Máy trộn│◄──── khóa con của lượt này
      │                │   f(R,K) │
      │                └────┬─────┘
      └──────► XOR ◄────────┘
      │                     │
      ▼                     ▼
   (Phải cũ)          (Trái cũ XOR kết quả máy trộn)
        └── hai xấp đổi chỗ cho nhau ──┘
```

Viết thành công thức cho lượt thứ `i`:

```
L(i) = R(i-1)
R(i) = L(i-1) XOR f( R(i-1), K(i) )
```

### Bên trong "máy trộn" f

Máy trộn nhận 32 bit và khóa con 48 bit, làm lần lượt bốn việc:

**Việc 1 – Nở ra.** 32 bit được sao chép bớt một số bit để thành 48 bit, cho vừa với khóa con.

**Việc 2 – Trộn khóa.** 48 bit này XOR với khóa con của lượt.

**Việc 3 – Tra bảng.** Chia 48 bit thành 8 nhóm 6 bit; mỗi nhóm đi vào một hộp thay thế (S-box) riêng và co lại còn 4 bit. Đây là bước duy nhất **không tuyến tính**, giữ vai trò "bộ não" gây khó cho kẻ phá mã.

**Việc 4 – Xáo vị trí.** 32 bit đầu ra bị hoán vị theo bảng P cố định.

### Trước và sau 16 lượt

- **Trước:** bản rõ đi qua hoán vị đầu (IP) để xáo sơ bộ.

- **Sau:** hai xấp bài được đổi chỗ lần cuối rồi đi qua hoán vị cuối (IP⁻¹), ra bản mã 64 bit.

### Lịch khóa con

Khóa DES ghi 64 bit nhưng 8 bit chỉ để kiểm tra lỗi, nên **khóa thật chỉ 56 bit**. Từ 56 bit ấy, DES cắt đôi, dịch vòng từng nửa qua mỗi lượt, rồi chọn ra 48 bit để làm khóa con `K(1)…K(16)`.

### Giải mã: chạy lại chính cỗ máy đó

Điểm hay của Feistel: **giải mã dùng đúng thuật toán mã hóa**, chỉ cần dùng lịch khóa theo thứ tự **ngược lại** (`K16` trước, `K1` sau). Lý do là phép XOR "tự hủy": `A XOR B XOR B = A`.

### Vì sao DES nghỉ hưu?

- Chỉ có `2^56` khóa để thử. Năm 1998, một cỗ máy chuyên dụng đã dò ra khóa DES trong vài ngày, và máy hiện đại còn nhanh hơn nhiều.

- Bản vá tạm là **3DES** (mã hóa ba lần liên tiếp), nhưng chậm và khối 64 bit quá nhỏ; NIST đã khuyến cáo ngừng dùng.

---

## 1.2 AES

### Lai lịch

AES là tên chuẩn của thuật toán **Rijndael** (Vincent Rijmen và Joan Daemen), được NIST chọn năm 2001 để thay DES, công bố trong tài liệu **FIPS-197**.

### Ba phiên bản

| Phiên bản | Độ dài khóa | Số lượt (vòng) |
|:---:|:---:|:---:|
| AES-128 | 128 bit | 10 |
| AES-192 | 192 bit | 12 |
| AES-256 | 256 bit | 14 |

Ở cả ba phiên bản, **khối dữ liệu luôn là 128 bit = 16 byte**.

### Sàn nhào bột: bảng 4×4

16 byte của một khối được xếp vào bảng 16 ô, đi **từng cột một** từ trên xuống:

```
 b0  b4  b8   b12
 b1  b5  b9   b13
 b2  b6  b10  b14
 b3  b7  b11  b15
```

Khác với DES chỉ đụng vào một nửa khối mỗi lượt, **mỗi lượt của AES nhào cả 16 byte cùng lúc**.

### Bốn động tác của mỗi lượt

| Động tác | Tên gốc | Làm gì | Để làm gì |
|---|---|---|---|
| **Thay** | SubBytes | Mỗi ô tra vào một bảng tra 256 phần tử (S-box) để đổi thành giá trị khác | Tạo tính **phi tuyến**, làm rối quan hệ giữa khóa và bản mã |
| **Trượt** | ShiftRows | Hàng 0 đứng yên, hàng 1 trượt trái 1 ô, hàng 2 trượt trái 2 ô, hàng 3 trượt trái 3 ô | Đưa byte sang **cột khác** để bước sau có cái mà trộn |
| **Khuấy** | MixColumns | Mỗi cột được nhân với một ma trận cố định trong trường GF(2⁸) | **Khuếch tán**: đổi một byte thì cả cột đổi theo |
| **Đóng dấu** | AddRoundKey | XOR bảng với khóa của lượt | Đưa **bí mật của khóa** vào dữ liệu |

Ma trận dùng cho động tác "Khuấy":

```
| 2 3 1 1 |   | a0 |
| 1 2 3 1 | × | a1 |
| 1 1 2 3 |   | a2 |
| 3 1 1 2 |   | a3 |
```

S-box của AES không phải bảng số tùy hứng. Nó được dựng từ **phép nghịch đảo trong GF(2⁸)** cộng thêm một biến đổi affine, nhờ vậy có tính chất toán học tốt chống các kiểu tấn công phổ biến.

### Toàn bộ quy trình mã hóa

```
Đóng dấu(khóa 0)

Lặp cho lượt 1 → (Nr - 1):
    Thay → Trượt → Khuấy → Đóng dấu(khóa lượt đó)

Lượt cuối (bỏ Khuấy):
    Thay → Trượt → Đóng dấu(khóa Nr)
```

### Quy trình giải mã: chạy ngược cuốn băng

Mỗi động tác đều có "động tác ngược", giải mã chỉ cần **chạy chúng theo thứ tự đảo lại**:

```
Đóng dấu(khóa Nr)

Lặp cho lượt (Nr - 1) → 1:
    Trượt ngược → Thay ngược → Đóng dấu(khóa lượt đó) → Khuấy ngược

Lượt cuối:
    Trượt ngược → Thay ngược → Đóng dấu(khóa 0)
```

Chi tiết cần nhớ:

- **Trượt ngược** trượt hàng sang phải.

- **Thay ngược** dùng S-box nghịch đảo.

- **Khuấy ngược** dùng ma trận có hệ số 14, 11, 13, 9.

### Lịch khóa (Key Expansion)

Từ khóa gốc, AES "kéo dài" ra thành `4 × (Nr + 1)` từ 32 bit. Cứ đến vị trí là bội của `Nk` (số từ của khóa), nó **xoay** một từ, cho qua S-box rồi XOR thêm hằng số `Rcon`. Các vị trí còn lại chỉ XOR hai từ cũ với nhau. Nhờ đó chỉ từ một khóa ngắn mà có đủ khóa cho mọi lượt.

### DES và AES khác nhau ở đâu?

| Điểm so sánh | DES | AES |
|---|---|---|
| Cách xáo | Feistel: mỗi lượt chỉ biến đổi một nửa khối | SPN: mỗi lượt biến đổi toàn bộ khối |
| Khối | 64 bit | 128 bit |
| Khóa thật sự | 56 bit | 128 / 192 / 256 bit |
| Số lượt | 16 | 10 / 12 / 14 |
| Giải mã | Dùng lại mạch mã hóa với khóa đảo thứ tự | Cần các phép biến đổi ngược riêng |
| Tình trạng | ❌ Đã lỗi thời | ✅ Chuẩn đang dùng toàn cầu |

---

## 1.3 Cài đặt AES bằng Python

> **Phạm vi:** đúng theo yêu cầu đặc biệt, chỉ AES được viết thành code. DES và RSA chỉ trình bày nguyên lý ở trên và dưới.

### Cách tổ chức chương trình

Code chia thành 5 khối rõ ràng, đọc từ trên xuống là thấy đúng tiến trình lý thuyết:

**Khối 1.** Toán nền: phép nhân trong GF(2⁸).

**Khối 2.** Tự **sinh S-box** bằng tính toán (tìm nghịch đảo rồi áp biến đổi affine), không chép bảng số.

**Khối 3.** Hàm đổi qua lại giữa `bytes` và ma trận 4×4.

**Khối 4.** Lớp `AES` gồm lịch khóa, bốn động tác, mã hóa / giải mã một khối, và mã hóa chuỗi dài theo chế độ **CBC** có đệm PKCS#7.

**Khối 5.** Phần chạy thử tự kiểm tra kết quả.

### Kết quả chạy thực tế

<img width="1917" height="1078" alt="image" src="https://github.com/user-attachments/assets/fc8ae040-fd02-4e9d-8d4c-9e934b589ba8" />

Ba dòng đầu cho thấy cài đặt **khớp từng byte** với vector chuẩn trong FIPS-197 ở cả ba độ dài khóa. Bản mã ở dòng 4 khác nhau mỗi lần chạy vì khóa và IV được sinh ngẫu nhiên.

```
AES-128: khop vector chuẩn -> 69c4e0d86a7b0430d8cdb78070b4c55a
AES-192: khop vector chuẩn -> dda97ca4864cdfe06eaf70a0ec0d7191
AES-256: khop vector chuẩn -> 8ea2b7ca516745bfeafc49904b496089
Bản mã : (chuỗi hex ngẫu nhiên, khác nhau mỗi lần chạy)
Giải mã: Bảo mật thông tin – học AES bằng cách tự cài đặt
Đổi 1 bit đầu vào -> bản mã khác 65/128 bit
```

### Hiệu ứng thác đổ (avalanche)

Dòng cuối cùng là điểm đáng chú ý: **chỉ đổi 1 bit** của bản rõ mà **65/128 bit** của bản mã bị đổi theo, tức xấp xỉ một nửa. Đó chính là dấu hiệu của một thuật toán trộn tốt, tác dụng của bộ đôi *Thay + Khuấy* qua nhiều lượt.

### Ví dụ dùng ở chương trình khác

```python
import os
from aes_moi import AES

khoa = os.urandom(32)                       # khóa AES-256
may = AES(khoa)

ban_ma = may.ma_hoa("Xin chào Minh".encode("utf-8"))
print(may.giai_ma(ban_ma).decode("utf-8"))  # Xin chào Minh
```

---

### 2. Tìm hiểu về thuật toán mã hoá bất đối xứng RSA nguyên lý sinh cặp khoá bí mật, công khai

## 2.1 Ý tưởng "ổ khóa mở"

Nhớ lại nút thắt của Chặng 1: làm sao đưa chìa cho nhau an toàn?

RSA xoay bài toán theo hướng khác. **Minh không đưa chìa cho ai cả.** Thay vào đó, Minh làm ra hàng loạt **ổ khóa đang mở** rồi treo công khai cho cả thế giới lấy:

- Ổ khóa mở đó là **khóa công khai**. Ai cũng bấm khóa lại được.

- Chiếc chìa duy nhất mở được nó là **khóa bí mật**, Minh giữ kín và không đưa cho ai.

Lan chỉ việc lấy ổ khóa của Minh, khóa hộp thư lại rồi gửi đi. Tùng có nhặt được hộp thì cũng bó tay, vì **bấm khóa thì dễ, mở khóa thì cần chìa riêng**.

| | Khóa công khai | Khóa bí mật |
|---|:---:|:---:|
| Ký hiệu | PU = (e, n) | PR = (d, n) |
| Ai biết? | Cả thế giới | Chỉ chủ nhân |
| Dùng để | Mã hóa, kiểm tra chữ ký | Giải mã, tạo chữ ký |

## 2.2 Nền tảng toán học

Sức mạnh của RSA đến từ một sự bất đối xứng của toán học:

- **Nhân** hai số nguyên tố khổng lồ với nhau thì **nhanh**.

- Có tích rồi mà **tìm lại** hai thừa số thì gần như **bất khả thi** khi các số đủ lớn.

Khóa RSA an toàn khi kẻ tấn công chỉ biết tích `n` mà không thể phân tích nó ra được.

## 2.3 Công thức 6 bước sinh cặp khóa

**Bước 1 – Chọn hai số nguyên tố** lớn, khác nhau: `p` và `q`.

**Bước 2 – Nhân chúng:** `n = p × q`. Số `n` này sẽ có mặt trong cả hai khóa.

**Bước 3 – Tính "số lượng đường ra":**

```
φ(n) = (p − 1) × (q − 1)
```

**Bước 4 – Chọn số mũ công khai `e`** sao cho `1 < e < φ(n)` và `e` **nguyên tố cùng nhau** với `φ(n)`. Thực tế người ta hay dùng `e = 65537`.

**Bước 5 – Tìm số mũ bí mật `d`** là nghịch đảo của `e` theo modulo `φ(n)`:

```
d × e ≡ 1  (mod φ(n))
```

`d` được tìm bằng thuật toán Euclid mở rộng.

**Bước 6 – Công bố và cất giữ:**

- Công bố **(e, n)**.

- Giấu kín **(d, n)**, và hủy sạch `p`, `q`, `φ(n)` vì lộ một trong ba thứ này là lộ luôn `d`.

## 2.4 Mã hóa và giải mã

```
Mã hóa  (ai cũng làm được):  C = M^e  mod n
Giải mã (chỉ chủ khóa làm):  M = C^d  mod n
```

Vì sao đảo ngược đúng? Do `e × d = 1 + k·φ(n)` nên theo định lý Euler, `M^(e·d) ≡ M (mod n)`.

Điều kiện: thông điệp `M` phải được đổi thành số nguyên nhỏ hơn `n`.

## 2.5 Chạy thử với số nhỏ

Con số nhỏ để bạn đọc có thể kiểm tra bằng tay (thực tế `p`, `q` dài hàng trăm chữ số):

| Việc cần làm | Phép tính | Kết quả |
|---|---|:---:|
| Chọn hai số nguyên tố | p = 7, q = 19 | |
| Tính n | 7 × 19 | **133** |
| Tính φ(n) | 6 × 18 | **108** |
| Chọn e | gcd(5, 108) = 1 | **5** |
| Tìm d | 5 × d ≡ 1 (mod 108) | **65** |
| Khóa công khai | (e, n) | **(5, 133)** |
| Khóa bí mật | (d, n) | **(65, 133)** |

Kiểm tra `d`: `5 × 65 = 325 = 3 × 108 + 1`, đúng là dư 1.

**Lan mã hóa `M = 9`:**

```
C = 9^5 mod 133 = 59049 mod 133 = 130
```

**Minh giải mã `C = 130`:**

```
M = 130^65 mod 133 = 9
```

Đúng bản rõ ban đầu.

## 2.6 Tùng có phá được không?

Tùng biết `(5, 133)`. Để tìm `d`, Tùng cần `φ(n)`, mà muốn có `φ(n)` thì phải phân tích `133 = 7 × 19`. Với số nhỏ như thế, việc này làm trong tích tắc. Nhưng với `n` dài 2048 bit thì không máy tính nào hiện nay làm nổi.

## 2.7 Ba điều phải nhớ khi dùng RSA thật

- **Khóa đủ dài:** tối thiểu 2048 bit, hệ thống dùng lâu dài nên chọn 3072 bit.

- **Không dùng RSA "trần".** Bắt buộc có đệm ngẫu nhiên: **OAEP** cho mã hóa, **PSS** cho chữ ký.

- **RSA chỉ ôm được dữ liệu nhỏ** (nhỏ hơn `n` trừ phần đệm). Đây là lý do nó không thể một mình mã hóa file lớn, và cũng là cớ để nó bắt tay với AES ở Chặng 3.

---


### 3. Trình bày các mô hình hình áp dụng thuật toán RSA xác thực người gửi, xác thực người nhận, cả 2 so sánh thời gian mã hoá/giải mã của RSA với AES đưa ra các dùng kết hợp sức mạnh của RSA và AES

Quy ước cho chặng này:

- **Lan** là người gửi, có cặp khóa `PU_L` (công khai) và `PR_L` (bí mật).

- **Minh** là người nhận, có cặp khóa `PU_M` và `PR_M`.

- **Tùng** là kẻ nghe lén trên đường truyền.

## 3.1 Ba cách dùng RSA

Điểm mấu chốt để phân biệt ba mô hình là **ai dùng khóa nào**. Chỉ cần nhớ hai quy tắc:

> 🔒 **Muốn giữ bí mật → khóa bằng khóa CÔNG KHAI của người nhận.**
>
> ✍️ **Muốn chứng minh mình là mình → ký bằng khóa BÍ MẬT của người gửi.**

### Mô hình A – Con dấu của Lan: xác thực người gửi

**Câu hỏi nó trả lời:** *"Thư này có đúng do Lan viết và không bị ai sửa không?"*

**Cách làm:** Lan băm tin nhắn ra một "dấu vân tay" ngắn rồi **ký bằng khóa bí mật `PR_L`**. Ai có khóa công khai của Lan đều kiểm tra được chữ ký, nhưng chỉ Lan mới tạo ra được nó.

```
LAN                                                   MINH
 │  h = Hash(M)                                        │
 │  S = Ký(PR_L, h)                                    │
 │ ─────────────────  gửi (M, S)  ───────────────────► │
 │                                                     │  h1 = Hash(M)
 │                                                     │  h2 = Giải(PU_L, S)
 │                                                     │  h1 = h2 ?
 │                                                     │  ├─ bằng nhau: đúng Lan, nội dung nguyên vẹn
 │                                                     │  └─ khác nhau: giả mạo hoặc đã bị sửa
```

| Đạt được | Không đạt được |
|---|---|
| ✅ Biết chắc người gửi là Lan | ❌ Không giữ bí mật: `M` đi nguyên văn, ai cũng đọc được |
| ✅ Nội dung không bị sửa | |
| ✅ Lan không chối được là mình đã gửi | |

Người ta ký lên **giá trị băm** thay vì cả bản tin, vì RSA chậm và bị giới hạn kích thước dữ liệu.

### Mô hình B – Hộp thư của Minh: xác thực người nhận

**Câu hỏi nó trả lời:** *"Làm sao chắc chỉ Minh đọc được?"*

**Cách làm:** Lan **mã hóa bằng khóa công khai `PU_M`**. Chỉ người giữ `PR_M` là Minh mới giải được, nên đúng người nhận mới đọc được thư.

```
LAN                                                   MINH
 │  C = Mã hóa(PU_M, M)                                │
 │ ──────────────────  gửi C  ───────────────────────► │
 │                                                     │  M = Giải mã(PR_M, C)
 │
 │  Tùng bắt được C nhưng không có PR_M → không đọc được
```

| Đạt được | Không đạt được |
|---|---|
| ✅ Bí mật: chỉ Minh đọc được | ❌ Không biết ai gửi: `PU_M` công khai, Tùng cũng tạo được `C` và đóng giả Lan |

### Mô hình C – Ký rồi niêm phong: xác thực cả hai

**Câu hỏi nó trả lời:** *"Vừa muốn bí mật, vừa muốn chắc chắn của Lan gửi?"*

**Cách làm:** ghép hai mô hình: Lan **ký bằng `PR_L`** trước, rồi **niêm phong bằng `PU_M`**.

```
LAN                                                    MINH
 │  S = Ký(PR_L, Hash(M))                               │
 │  C = Mã hóa(PU_M, M kèm S)                           │
 │ ──────────────────  gửi C  ───────────────────────► │
 │                                                      │  (M, S) = Giải mã(PR_M, C)
 │                                                      │  Kiểm tra S bằng PU_L
```

| Mục tiêu | Mô hình A | Mô hình B | Mô hình C |
|---|:---:|:---:|:---:|
| Bí mật nội dung | ❌ | ✅ | ✅ |
| Xác thực người gửi | ✅ | ❌ | ✅ |
| Toàn vẹn và chống chối bỏ | ✅ | ❌ | ✅ |

---

## 3.2 Cuộc đua tốc độ: AES và RSA

### Vì sao AES thắng áp đảo?

**AES** chỉ làm những việc mà CPU cực giỏi: tra bảng, dịch byte, XOR. Nhiều CPU còn có sẵn **lệnh phần cứng AES-NI** chuyên cho nó.

**RSA** thì phải tính **lũy thừa modular trên số nguyên hàng nghìn bit** (`M^e mod n`, `C^d mod n`). Một phép nhân số khổng lồ đã nặng, mà lũy thừa lại lặp rất nhiều phép nhân như vậy.

### Ngay trong RSA, hai chiều cũng chênh lệch

- Chiều dùng **khóa công khai**: `e` nhỏ (như 65537) nên tính tương đối nhanh.

- Chiều dùng **khóa bí mật**: `d` lớn cỡ `n` nên chậm hơn hẳn. Chi phí tăng gần như theo **lập phương** độ dài khóa: tăng khóa từ 2048 lên 4096 bit làm chiều này chậm đi khoảng 6–8 lần.

### Bảng đối chiếu

| Tiêu chí | AES | RSA |
|---|---|---|
| Họ thuật toán | Đối xứng | Bất đối xứng |
| Khóa | 1 khóa chung | Cặp khóa công khai / bí mật |
| Tốc độ | Rất nhanh: cỡ **hàng trăm MB/s đến GB/s** khi có AES-NI | Rất chậm: **dưới 1 MB/s** nếu quy đổi ra thông lượng dữ liệu |
| Mức chênh | Nhanh hơn RSA cỡ **hàng trăm đến hàng nghìn lần** | |
| Cỡ dữ liệu xử lý | Không giới hạn (chia khối, nối tiếp) | Nhỏ hơn độ dài `n` trừ đệm, khoảng 190 byte với RSA-2048 + OAEP-SHA256 |
| Trao đổi khóa | ❌ Khó | ✅ Dễ |
| Chữ ký số | ❌ Không có | ✅ Có |
| Việc phù hợp | Chở **dữ liệu** | Trao **khóa**, ký **chữ ký** |

> 📝 Các con số tốc độ chỉ nhằm cho thấy **bậc độ lớn**. Kết quả chính xác phụ thuộc CPU, thư viện và cách cài đặt.

### RSA cần khóa dài hơn nhiều để đạt cùng độ an toàn

Đây là một lý do khác khiến RSA nặng nề (theo khuyến nghị NIST SP 800-57):

| Mức an toàn tương đương | Khóa AES | Khóa RSA |
|:---:|:---:|:---:|
| 112 bit | | 2048 bit |
| 128 bit | 128 bit | 3072 bit |
| 192 bit | 192 bit | 7680 bit |
| 256 bit | 256 bit | 15360 bit |

### Tự đo trên máy của mình

Công cụ OpenSSL có sẵn lệnh đo, chạy ở terminal:

```bash
openssl speed aes-256-cbc rsa2048
```

AES được báo theo **byte trên giây**, còn RSA báo theo **số lần ký và kiểm tra mỗi giây**. Muốn đặt lên bàn cân chung, hãy nhân số lần RSA/giây với số byte mỗi lần (khoảng 190) để ra thông lượng tương đương.

---

## 3.3 Cái bắt tay lai: RSA gửi chìa, AES chở hàng

### Điểm mạnh yếu bù nhau

| | Mạnh ở | Yếu ở |
|---|---|---|
| **AES** | Nhanh, chở được dữ liệu lớn | Không có cách tự trao chìa an toàn |
| **RSA** | Trao khóa và ký số rất tiện | Chậm, chỉ ôm được dữ liệu nhỏ |

Ghép lại thì "hết chỗ hở": **AES là chiếc xe tải chở hàng, RSA là người giao chìa khóa xe** bằng một phong bì mà chỉ người nhận mở được. Khóa AES chỉ 16 hoặc 32 byte, vừa vặn để RSA xử lý.

### Cuộc trao đổi diễn ra thế nào?

**Phía Lan (gửi):**

1. Lan **bốc ngẫu nhiên** một khóa phiên `Ks` (ví dụ 256 bit), chỉ dùng cho lần này.

2. Lan **mã hóa dữ liệu bằng AES**: `C_data = AES(Ks, M)`.

3. Lan **bỏ chìa `Ks` vào phong bì** bằng RSA: `C_key = RSA(PU_M, Ks)`.

4. (Nếu cần xác thực) Lan ký: `S = Ký(PR_L, Hash(M))`.

5. Lan gửi `C_key`, `C_data` (và `S`).

**Phía Minh (nhận):**

1. Minh **mở phong bì** bằng khóa bí mật: `Ks = RSA⁻¹(PR_M, C_key)`.

2. Minh **giải mã dữ liệu** bằng AES: `M = AES⁻¹(Ks, C_data)`.

3. Minh **kiểm tra chữ ký** của Lan bằng `PU_L` và so với `Hash(M)`.

### Sơ đồ tổng thể

```
        LAN                                                       MINH
  ┌────────────┐                                            ┌────────────┐
  │  Bản tin M │                                            │  Bản tin M │
  └─────┬──────┘                                            └─────▲──────┘
        │ AES với Ks                                              │ AES⁻¹ với Ks
        ▼                                                         │
     C_data ═════════════════════ gửi ═══════════════════════► C_data
                                                                  ▲
  Ks (ngẫu nhiên)                                                 │ Ks khôi phục được
        │ RSA với PU_M                                            │
        ▼                                                         │
     C_key ══════════════════════ gửi ═══════════════════════► RSA⁻¹ với PR_M

  Hash(M) ─► ký bằng PR_L ─► S ═══ gửi ═══► kiểm tra bằng PU_L, so với Hash(M)
```

### Được gì từ cách làm này?

- ✅ **Nhanh:** phần dữ liệu lớn giao cho AES.

- ✅ **Không cần kênh bí mật riêng:** RSA lo việc đưa chìa qua đường công cộng.

- ✅ **Đủ bộ bảo mật:** bí mật (AES + RSA), xác thực và chống chối bỏ (chữ ký), toàn vẹn (hàm băm).

- ✅ **Khóa dùng một lần:** mỗi phiên có `Ks` mới, lộ phiên này không kéo theo lộ các phiên khác.

### Ngoài đời thực

- **PGP / GPG** (bảo mật email): nội dung mã hóa bằng khóa đối xứng, khóa đó được bọc bằng khóa công khai của người nhận. Đây gần như đúng nguyên mẫu của mô hình lai ở trên.

- **HTTPS / TLS:** dữ liệu trên đường truyền được mã hóa bằng thuật toán đối xứng như AES, còn khóa phiên được thỏa thuận bằng mật mã khóa công khai. Lưu ý: TLS 1.3 bỏ hình thức "gói khóa bằng RSA" và chuyển sang trao đổi khóa Diffie–Hellman tạm thời, còn RSA chủ yếu dùng để **ký** xác thực máy chủ.

- **SSH, VPN, ứng dụng nhắn tin mã hóa:** đều xoay quanh cùng một tư tưởng: khóa công khai để bắt tay, khóa đối xứng để chở dữ liệu.

---

# 🏁 Tổng kết

- **DES** mở đường cho mật mã khối nhưng khóa 56 bit đã quá yếu. **AES** kế nhiệm với khối 128 bit, khóa tới 256 bit, mỗi lượt nhào trộn toàn bộ khối.

- **RSA** giải nút thắt mà mã hóa đối xứng bó tay: **trao khóa qua môi trường công cộng** và **chữ ký số**, dựa trên độ khó của việc phân tích số nguyên lớn.

- Ba cách dùng RSA cho ba mục tiêu: **ký** để xác thực người gửi, **mã hóa bằng khóa công khai** để bảo mật cho người nhận, và **kết hợp cả hai** khi cần đủ hết.

- Vì RSA chậm và giới hạn dữ liệu, thực tế luôn dùng **mô hình lai**: **AES chở dữ liệu, RSA giao khóa và ký**.

---
