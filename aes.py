
import os

# ============ 1. Toán học nền: phép nhân trong GF(2^8) ============
def nhan_gf(a, b):
    """Nhân hai byte trong GF(2^8), đa thức tối giản x^8 + x^4 + x^3 + x + 1."""
    kq = 0
    for _ in range(8):
        if b & 1:
            kq ^= a
        cao = a & 0x80
        a = (a << 1) & 0xFF
        if cao:
            a ^= 0x1B
        b >>= 1
    return kq


def xoay_trai_byte(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xFF


# ============ 2. S-box: nghịch đảo nhân + biến đổi affine ============
def _tao_sbox():
    nghich_dao = [0] * 256
    for a in range(1, 256):
        for b in range(1, 256):
            if nhan_gf(a, b) == 1:
                nghich_dao[a] = b
                break
    sbox = []
    for x in range(256):
        b = nghich_dao[x]
        sbox.append(b ^ xoay_trai_byte(b, 1) ^ xoay_trai_byte(b, 2)
                    ^ xoay_trai_byte(b, 3) ^ xoay_trai_byte(b, 4) ^ 0x63)
    return sbox


SBOX = _tao_sbox()
SBOX_NGUOC = [0] * 256
for i, v in enumerate(SBOX):
    SBOX_NGUOC[v] = i

# Bảng nhân sẵn để MixColumns chạy nhanh hơn
BANG_NHAN = {k: [nhan_gf(x, k) for x in range(256)] for k in (1, 2, 3, 9, 11, 13, 14)}

HE_SO_TRON = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
HE_SO_TRON_NGUOC = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]


# ============ 3. Chuyển đổi bytes <-> ma trận 4x4 ============
def bytes_sang_ma_tran(b):
    return [[b[hang + 4 * cot] for cot in range(4)] for hang in range(4)]


def ma_tran_sang_bytes(m):
    return bytes(m[hang][cot] for cot in range(4) for hang in range(4))


# ============ 4. Lớp AES ============
class AES:
    def __init__(self, khoa):
        if len(khoa) not in (16, 24, 32):
            raise ValueError("Khóa phải dài 16, 24 hoặc 32 byte")
        self.nk = len(khoa) // 4
        self.so_vong = self.nk + 6
        self.khoa_vong = self._mo_rong_khoa(khoa)

    # ---- Sinh các khóa vòng ----
    def _mo_rong_khoa(self, khoa):
        w = [list(khoa[4 * i:4 * i + 4]) for i in range(self.nk)]
        hang_so = 1
        for i in range(self.nk, 4 * (self.so_vong + 1)):
            t = list(w[i - 1])
            if i % self.nk == 0:
                t = [SBOX[x] for x in t[1:] + t[:1]]
                t[0] ^= hang_so
                hang_so = BANG_NHAN[2][hang_so]
            elif self.nk > 6 and i % self.nk == 4:
                t = [SBOX[x] for x in t]
            w.append([a ^ b for a, b in zip(w[i - self.nk], t)])
        khoa_vong = []
        for r in range(self.so_vong + 1):
            cac_cot = w[4 * r:4 * r + 4]
            khoa_vong.append([[cac_cot[c][h] for c in range(4)] for h in range(4)])
        return khoa_vong

    # ---- Bốn phép biến đổi (và nghịch đảo) ----
    @staticmethod
    def _thay_byte(m, hop):
        return [[hop[x] for x in hang] for hang in m]

    @staticmethod
    def _dich_hang(m):
        return [hang[i:] + hang[:i] for i, hang in enumerate(m)]

    @staticmethod
    def _dich_hang_nguoc(m):
        return [hang[-i:] + hang[:-i] if i else hang[:] for i, hang in enumerate(m)]

    @staticmethod
    def _tron_cot(m, he_so):
        kq = [[0] * 4 for _ in range(4)]
        for cot in range(4):
            for hang in range(4):
                v = 0
                for k in range(4):
                    v ^= BANG_NHAN[he_so[hang][k]][m[k][cot]]
                kq[hang][cot] = v
        return kq

    @staticmethod
    def _cong_khoa(m, khoa):
        return [[m[h][c] ^ khoa[h][c] for c in range(4)] for h in range(4)]

    # ---- Mã hóa / giải mã 1 khối 16 byte ----
    def ma_hoa_khoi(self, khoi):
        m = self._cong_khoa(bytes_sang_ma_tran(khoi), self.khoa_vong[0])
        for v in range(1, self.so_vong):
            m = self._thay_byte(m, SBOX)
            m = self._dich_hang(m)
            m = self._tron_cot(m, HE_SO_TRON)
            m = self._cong_khoa(m, self.khoa_vong[v])
        m = self._thay_byte(m, SBOX)
        m = self._dich_hang(m)
        m = self._cong_khoa(m, self.khoa_vong[self.so_vong])
        return ma_tran_sang_bytes(m)

    def giai_ma_khoi(self, khoi):
        m = self._cong_khoa(bytes_sang_ma_tran(khoi), self.khoa_vong[self.so_vong])
        for v in range(self.so_vong - 1, 0, -1):
            m = self._dich_hang_nguoc(m)
            m = self._thay_byte(m, SBOX_NGUOC)
            m = self._cong_khoa(m, self.khoa_vong[v])
            m = self._tron_cot(m, HE_SO_TRON_NGUOC)
        m = self._dich_hang_nguoc(m)
        m = self._thay_byte(m, SBOX_NGUOC)
        m = self._cong_khoa(m, self.khoa_vong[0])
        return ma_tran_sang_bytes(m)

    # ---- Mã hóa chuỗi dài: chế độ CBC + đệm PKCS#7 ----
    def ma_hoa(self, ban_ro, iv=None):
        iv = iv or os.urandom(16)
        thieu = 16 - len(ban_ro) % 16
        du_lieu = ban_ro + bytes([thieu]) * thieu
        truoc, ket_qua = iv, b""
        for i in range(0, len(du_lieu), 16):
            khoi = bytes(x ^ y for x, y in zip(du_lieu[i:i + 16], truoc))
            truoc = self.ma_hoa_khoi(khoi)
            ket_qua += truoc
        return iv + ket_qua

    def giai_ma(self, ban_ma):
        iv, phan_ma = ban_ma[:16], ban_ma[16:]
        truoc, ket_qua = iv, b""
        for i in range(0, len(phan_ma), 16):
            khoi = phan_ma[i:i + 16]
            ket_qua += bytes(x ^ y for x, y in zip(self.giai_ma_khoi(khoi), truoc))
            truoc = khoi
        n = ket_qua[-1]
        if not 1 <= n <= 16 or ket_qua[-n:] != bytes([n]) * n:
            raise ValueError("Sai khóa hoặc bản mã đã bị sửa")
        return ket_qua[:-n]


# ============ 5. Chạy thử ============
def dem_bit_khac(a, b):
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


if __name__ == "__main__":
    # (a) Đối chiếu vector chuẩn FIPS-197, Phụ lục C
    ban_ro = bytes.fromhex("00112233445566778899aabbccddeeff")
    chuan = {16: "69c4e0d86a7b0430d8cdb78070b4c55a",
             24: "dda97ca4864cdfe06eaf70a0ec0d7191",
             32: "8ea2b7ca516745bfeafc49904b496089"}
    for do_dai, mong_doi in chuan.items():
        aes = AES(bytes(range(do_dai)))
        ma = aes.ma_hoa_khoi(ban_ro)
        assert ma.hex() == mong_doi and aes.giai_ma_khoi(ma) == ban_ro
        print(f"AES-{do_dai * 8}: khop vector chuẩn -> {ma.hex()}")

    # (b) Mã hóa một câu tiếng Việt bằng CBC
    aes = AES(os.urandom(32))
    cau = "Bảo mật thông tin – học AES bằng cách tự cài đặt".encode("utf-8")
    ma = aes.ma_hoa(cau)
    print("Bản mã :", ma.hex())
    print("Giải mã:", aes.giai_ma(ma).decode("utf-8"))

    # (c) Hiệu ứng thác đổ: đổi đúng 1 bit đầu vào, xem bản mã đổi bao nhiêu bit
    aes = AES(bytes(range(16)))
    a = aes.ma_hoa_khoi(bytes(16))
    b = aes.ma_hoa_khoi(bytes([1]) + bytes(15))
    print(f"Đổi 1 bit đầu vào -> bản mã khác {dem_bit_khac(a, b)}/128 bit")