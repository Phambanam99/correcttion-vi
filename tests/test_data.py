# -*- coding: utf-8 -*-
"""
Bộ test dữ liệu cho Vietnamese Text Corrector
Bao gồm: 10 câu, 10 đoạn văn, 10 bài văn
Mỗi item có: input (văn bản lỗi) và expected (văn bản đúng)
"""

# =====================================================
# 10 CÂU ĐƠN (SENTENCES)
# =====================================================
SENTENCES = [
    {
        "id": 1,
        "input": "hom qua em di chua Huong",
        "expected": "Hôm qua em đi chùa Hương.",
        "errors": ["thiếu dấu", "địa danh"]
    },
    {
        "id": 2,
        "input": "toi la sinh vien truong dai hoc bach khoa",
        "expected": "Tôi là sinh viên trường Đại học Bách khoa.",
        "errors": ["thiếu dấu", "viết hoa danh từ riêng"]
    },
    {
        "id": 3,
        "input": "anh ay lam viec o thanh pho ho chi minh",
        "expected": "Anh ấy làm việc ở thành phố Hồ Chí Minh.",
        "errors": ["thiếu dấu", "địa danh"]
    },
    {
        "id": 4,
        "input": "con cho nha toi rat de thuong",
        "expected": "Con chó nhà tôi rất dễ thương.",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 5,
        "input": "me toi nau com rat ngon",
        "expected": "Mẹ tôi nấu cơm rất ngon.",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 6,
        "input": "hoc sinh can co gang hoc tap tot hon",
        "expected": "Học sinh cần cố gắng học tập tốt hơn.",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 7,
        "input": "ngay mai toi se di Ha Noi",
        "expected": "Ngày mai tôi sẽ đi Hà Nội.",
        "errors": ["thiếu dấu", "địa danh"]
    },
    {
        "id": 8,
        "input": "troi hom nay dep qua nhung hoi lanh",
        "expected": "Trời hôm nay đẹp quá nhưng hơi lạnh.",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 9,
        "input": "cuon sach nay rat hay va bo ich",
        "expected": "Cuốn sách này rất hay và bổ ích.",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 10,
        "input": "em gai toi nam nay hoc lop 5",
        "expected": "Em gái tôi năm nay học lớp 5.",
        "errors": ["thiếu dấu"]
    },
]

# =====================================================
# 10 ĐOẠN VĂN (PARAGRAPHS)
# =====================================================
PARAGRAPHS = [
    {
        "id": 1,
        "input": """hom qua toi di tham quan vinh Ha Long. Canh dep vo cung. Nuoc bien xanh ngat, nhung hon dao nho xinh xan noi len giua bien.""",
        "expected": """Hôm qua tôi đi tham quan vịnh Hạ Long. Cảnh đẹp vô cùng. Nước biển xanh ngắt, những hòn đảo nhỏ xinh xắn nổi lên giữa biển.""",
        "errors": ["thiếu dấu", "địa danh", "chính tả"]
    },
    {
        "id": 2,
        "input": """viet nam co nhieu danh lam thang canh noi tiếng. Tu bac vao nam, du khach co the ghe tham nhieu noi dep nhu Sa Pa, Hoi An, Da Lat.""",
        "expected": """Việt Nam có nhiều danh lam thắng cảnh nổi tiếng. Từ Bắc vào Nam, du khách có thể ghé thăm nhiều nơi đẹp như Sa Pa, Hội An, Đà Lạt.""",
        "errors": ["thiếu dấu", "địa danh"]
    },
    {
        "id": 3,
        "input": """mua xuan la mua dep nhat trong nam. Cay coi dau choi non, hoa no khap noi. Thoi tiet am ap, khong khi trong lanh.""",
        "expected": """Mùa xuân là mùa đẹp nhất trong năm. Cây cối đâm chồi nảy lộc, hoa nở khắp nơi. Thời tiết ấm áp, không khí trong lành.""",
        "errors": ["thiếu dấu", "chính tả"]
    },
    {
        "id": 4,
        "input": """cong nghe thong tin ngay cang phat trien. Dien thoai thong minh tro thanh vat dung khong the thieu. Moi nguoi deu co the ket noi voi nhau qua internet.""",
        "expected": """Công nghệ thông tin ngày càng phát triển. Điện thoại thông minh trở thành vật dụng không thể thiếu. Mọi người đều có thể kết nối với nhau qua internet.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 5,
        "input": """gia dinh toi co 4 nguoi: bo, me, anh trai va toi. Bo toi la ky su, me toi la giao vien. Anh trai toi dang hoc dai hoc.""",
        "expected": """Gia đình tôi có 4 người: bố, mẹ, anh trai và tôi. Bố tôi là kỹ sư, mẹ tôi là giáo viên. Anh trai tôi đang học đại học.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 6,
        "input": """moi ngay toi thuc day luc 6 gio sang. Sau khi danh rang rua mat, toi an sang roi di hoc. Buoi toi toi thuong hoc bai den 10 gio.""",
        "expected": """Mỗi ngày tôi thức dậy lúc 6 giờ sáng. Sau khi đánh răng rửa mặt, tôi ăn sáng rồi đi học. Buổi tối tôi thường học bài đến 10 giờ.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 7,
        "input": """the thao rat tot cho suc khoe. Chay bo, boi loi, da bong deu la nhung mon the thao pho bien. Moi nguoi nen tap the duc it nhat 30 phut moi ngay.""",
        "expected": """Thể thao rất tốt cho sức khỏe. Chạy bộ, bơi lội, đá bóng đều là những môn thể thao phổ biến. Mọi người nên tập thể dục ít nhất 30 phút mỗi ngày.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 8,
        "input": """am nhac co suc manh ky dieu. No co the lam ta vui, buon, hay thu gian. Nghe nhac giup giam stress va tang hieu qua lam viec.""",
        "expected": """Âm nhạc có sức mạnh kỳ diệu. Nó có thể làm ta vui, buồn, hay thư giãn. Nghe nhạc giúp giảm stress và tăng hiệu quả làm việc.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 9,
        "input": """doc sach la mot thoi quen tot. Sach giup ta mo mang kien thuc, hieu biet them ve the gioi. Moi nguoi nen doc sach it nhat 15 phut moi ngay.""",
        "expected": """Đọc sách là một thói quen tốt. Sách giúp ta mở mang kiến thức, hiểu biết thêm về thế giới. Mọi người nên đọc sách ít nhất 15 phút mỗi ngày.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 10,
        "input": """bao ve moi truong la trach nhiem cua moi nguoi. Chung ta can giam thieu rac thai nhua, trong nhieu cay xanh. Mot hanh dong nho cung co the tao nen su thay doi lon.""",
        "expected": """Bảo vệ môi trường là trách nhiệm của mọi người. Chúng ta cần giảm thiểu rác thải nhựa, trồng nhiều cây xanh. Một hành động nhỏ cũng có thể tạo nên sự thay đổi lớn.""",
        "errors": ["thiếu dấu"]
    },
]

# =====================================================
# 10 BÀI VĂN (ESSAYS)
# =====================================================
ESSAYS = [
    {
        "id": 1,
        "title": "Quê hương",
        "input": """que huong toi la mot lang nho nam ben dong song. Moi sang thuc day, toi nghe tieng chim hot, tieng ga gay. Khong khi trong lanh, mat me.

Truoc nha toi co mot cay bang lon. Mua he, toi thuong ngoi duoi goc cay doc sach. Mua thu, la vang roi day san. Tre em trong lang thuong choi dua duoi goc cay.

Toi rat yeu que huong minh. Du di dau toi cung luon nho ve noi day.""",
        "expected": """Quê hương tôi là một làng nhỏ nằm bên dòng sông. Mỗi sáng thức dậy, tôi nghe tiếng chim hót, tiếng gà gáy. Không khí trong lành, mát mẻ.

Trước nhà tôi có một cây bàng lớn. Mùa hè, tôi thường ngồi dưới gốc cây đọc sách. Mùa thu, lá vàng rơi đầy sân. Trẻ em trong làng thường chơi đùa dưới gốc cây.

Tôi rất yêu quê hương mình. Dù đi đâu tôi cũng luôn nhớ về nơi đây.""",
        "errors": ["thiếu dấu toàn bộ"]
    },
    {
        "id": 2,
        "title": "Mẹ tôi",
        "input": """me toi la nguoi phu nu hien lanh, dam dang. Ba luon thuc day som de chuan bi bua sang cho ca nha. Du ban ron the nao, me van luon quan tam den con cai.

me toi lam nghe may. Moi ngay ba phai lam viec tu 8 gio sang den 6 gio chieu. Ve nha, me lai tiep tuc nau com, don dep nha cua.

Toi thuong giup me lam viec nha. Toi hieu rang me da hy sinh rat nhieu cho gia dinh. Toi se co gang hoc tot de me vui long.""",
        "expected": """Mẹ tôi là người phụ nữ hiền lành, đảm đang. Bà luôn thức dậy sớm để chuẩn bị bữa sáng cho cả nhà. Dù bận rộn thế nào, mẹ vẫn luôn quan tâm đến con cái.

Mẹ tôi làm nghề may. Mỗi ngày bà phải làm việc từ 8 giờ sáng đến 6 giờ chiều. Về nhà, mẹ lại tiếp tục nấu cơm, dọn dẹp nhà cửa.

Tôi thường giúp mẹ làm việc nhà. Tôi hiểu rằng mẹ đã hy sinh rất nhiều cho gia đình. Tôi sẽ cố gắng học tốt để mẹ vui lòng.""",
        "errors": ["thiếu dấu", "viết hoa đầu câu"]
    },
    {
        "id": 3,
        "title": "Ngày Tết",
        "input": """tet nguyen dan la ngay le quan trong nhat cua nguoi Viet Nam. Truoc Tet, moi nha deu don dep, trang hoang nha cua. Duong pho tro nen nao nhiet, dong duc.

Dem giao thua, ca gia dinh toi quay quan ben nhau. Chung toi cung xem phao hoa, chuc nhau nam moi. Sang mung Mot, tre em deu duoc nhan li xi.

Toi rat thich Tet vi duoc nghi hoc va gap go ho hang. Khong khi Tet luc nao cung vui tuoi, am ap.""",
        "expected": """Tết Nguyên đán là ngày lễ quan trọng nhất của người Việt Nam. Trước Tết, mọi nhà đều dọn dẹp, trang hoàng nhà cửa. Đường phố trở nên náo nhiệt, đông đúc.

Đêm giao thừa, cả gia đình tôi quây quần bên nhau. Chúng tôi cùng xem pháo hoa, chúc nhau năm mới. Sáng mùng Một, trẻ em đều được nhận lì xì.

Tôi rất thích Tết vì được nghỉ học và gặp gỡ họ hàng. Không khí Tết lúc nào cũng vui tươi, ấm áp.""",
        "errors": ["thiếu dấu", "danh từ riêng"]
    },
    {
        "id": 4,
        "title": "Trường học",
        "input": """truong hoc cua toi nam tren mot con duong lon, rat dep. Co san rong voi nhieu cay xanh. Buoi sang, hoc sinh tap trung o san de chao co.

Lop toi co 40 ban. Co giao chu nhiem la co Lan, rat hien va tot bung. Co Lan day mon Toan, giang bai rat de hieu.

Toi rat thich di hoc vi duoc gap ban be va thay co. Truong hoc la noi giup em truong thanh moi ngay.""",
        "expected": """Trường học của tôi nằm trên một con đường lớn, rất đẹp. Có sân rộng với nhiều cây xanh. Buổi sáng, học sinh tập trung ở sân để chào cờ.

Lớp tôi có 40 bạn. Cô giáo chủ nhiệm là cô Lan, rất hiền và tốt bụng. Cô Lan dạy môn Toán, giảng bài rất dễ hiểu.

Tôi rất thích đi học vì được gặp bạn bè và thầy cô. Trường học là nơi giúp em trưởng thành mỗi ngày.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 5,
        "title": "Mùa hè",
        "input": """mua he la mua toi yeu thich nhat. Duoc nghi hoc, toi co the vui choi thoa thich. Moi ngay toi thuong di boi voi cac ban.

Mua he nam nay, gia dinh toi di du lich Nha Trang. Bien Nha Trang rat dep, nuoc xanh trong. Toi duoc tam bien, an hai san tuoi ngon.

Ky nghi he thuc su tuyet voi. Toi da co nhieu ky niem dep. Toi mong muon mua he nam sau se con vui hon.""",
        "expected": """Mùa hè là mùa tôi yêu thích nhất. Được nghỉ học, tôi có thể vui chơi thỏa thích. Mỗi ngày tôi thường đi bơi với các bạn.

Mùa hè năm nay, gia đình tôi đi du lịch Nha Trang. Biển Nha Trang rất đẹp, nước xanh trong. Tôi được tắm biển, ăn hải sản tươi ngon.

Kỳ nghỉ hè thực sự tuyệt vời. Tôi đã có nhiều kỷ niệm đẹp. Tôi mong muốn mùa hè năm sau sẽ còn vui hơn.""",
        "errors": ["thiếu dấu", "địa danh"]
    },
    {
        "id": 6,
        "title": "Ông bà",
        "input": """ong ba noi toi song o que. Moi dip he, toi thuong ve que tham ong ba. Ong ba da gia nhung van khoe manh, vui ve.

ong toi thich trong cay. Khu vuon nha ong co nhieu loai cay an qua. Ba noi thuong ke cho toi nghe nhung cau chuyen co tich.

Toi rat yeu ong ba. Toi mong ong ba luon khoe manh de toi con duoc ve tham.""",
        "expected": """Ông bà nội tôi sống ở quê. Mỗi dịp hè, tôi thường về quê thăm ông bà. Ông bà đã già nhưng vẫn khỏe mạnh, vui vẻ.

Ông tôi thích trồng cây. Khu vườn nhà ông có nhiều loại cây ăn quả. Bà nội thường kể cho tôi nghe những câu chuyện cổ tích.

Tôi rất yêu ông bà. Tôi mong ông bà luôn khỏe mạnh để tôi còn được về thăm.""",
        "errors": ["thiếu dấu", "viết hoa đầu câu"]
    },
    {
        "id": 7,
        "title": "Bạn thân",
        "input": """ban than cua toi ten la Minh. Chung toi hoc chung lop tu lop 1. Minh la mot nguoi ban tot bung va than thien.

Minh hoc gioi mon Toan. Moi khi toi gap bai kho, Minh deu giup toi. Chung toi thuong di choi, hoc bai cung nhau.

Toi hy vong tinh ban cua chung toi se mai ben vung. Mot nguoi ban tot that su quy gia.""",
        "expected": """Bạn thân của tôi tên là Minh. Chúng tôi học chung lớp từ lớp 1. Minh là một người bạn tốt bụng và thân thiện.

Minh học giỏi môn Toán. Mỗi khi tôi gặp bài khó, Minh đều giúp tôi. Chúng tôi thường đi chơi, học bài cùng nhau.

Tôi hy vọng tình bạn của chúng tôi sẽ mãi bền vững. Một người bạn tốt thật sự quý giá.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 8,
        "title": "Sách",
        "input": """sach la nguon tri thuc vo tan. Doc sach giup ta hieu biet them ve the gioi xung quanh. Moi quyen sach la mot nguoi thay.

Toi thich doc truyen co tich va truyen trinh tham. Moi toi truoc khi ngu, toi thuong doc sach khoang 30 phut.

Doc sach giup toi viet van tot hon. Ngon ngu cua toi cung phong phu hon. Toi khuyen moi nguoi nen doc sach moi ngay.""",
        "expected": """Sách là nguồn tri thức vô tận. Đọc sách giúp ta hiểu biết thêm về thế giới xung quanh. Mỗi quyển sách là một người thầy.

Tôi thích đọc truyện cổ tích và truyện trinh thám. Mỗi tối trước khi ngủ, tôi thường đọc sách khoảng 30 phút.

Đọc sách giúp tôi viết văn tốt hơn. Ngôn ngữ của tôi cũng phong phú hơn. Tôi khuyên mọi người nên đọc sách mỗi ngày.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 9,
        "title": "Môi trường",
        "input": """moi truong dang bi o nhiem nghiem trong. Rac thai nhua tran ngap khap noi. Khong khi o cac thanh pho lon cung bi o nhiem.

Chung ta can hanh dong ngay bay gio. Hay giam thieu su dung do nhua, trong nhieu cay xanh. Moi nguoi hay di xe dap thay vi xe may.

Bao ve moi truong la bao ve chinh chung ta. Hay cung nhau giu gin trai dat xanh sach dep.""",
        "expected": """Môi trường đang bị ô nhiễm nghiêm trọng. Rác thải nhựa tràn ngập khắp nơi. Không khí ở các thành phố lớn cũng bị ô nhiễm.

Chúng ta cần hành động ngay bây giờ. Hãy giảm thiểu sử dụng đồ nhựa, trồng nhiều cây xanh. Mọi người hãy đi xe đạp thay vì xe máy.

Bảo vệ môi trường là bảo vệ chính chúng ta. Hãy cùng nhau giữ gìn trái đất xanh sạch đẹp.""",
        "errors": ["thiếu dấu"]
    },
    {
        "id": 10,
        "title": "Ước mơ",
        "input": """moi nguoi deu co uoc mo rieng. Uoc mo cua toi la tro thanh mot bac si gioi. Toi muon chua benh cuu nguoi.

de thuc hien uoc mo, toi dang co gang hoc tap. Toi hoc gioi cac mon khoa hoc tu nhien. Toi cung doc nhieu sach ve y hoc.

Toi tin rang neu co gang, uoc mo se thanh hien thuc. Toi se khong bao gio tu bo uoc mo cua minh.""",
        "expected": """Mỗi người đều có ước mơ riêng. Ước mơ của tôi là trở thành một bác sĩ giỏi. Tôi muốn chữa bệnh cứu người.

Để thực hiện ước mơ, tôi đang cố gắng học tập. Tôi học giỏi các môn khoa học tự nhiên. Tôi cũng đọc nhiều sách về y học.

Tôi tin rằng nếu cố gắng, ước mơ sẽ thành hiện thực. Tôi sẽ không bao giờ từ bỏ ước mơ của mình.""",
        "errors": ["thiếu dấu", "viết hoa đầu câu"]
    },
]


def get_all_test_data():
    """Trả về tất cả dữ liệu test"""
    return {
        "sentences": SENTENCES,
        "paragraphs": PARAGRAPHS,
        "essays": ESSAYS
    }


def get_test_summary():
    """Trả về thống kê bộ test"""
    return {
        "total_sentences": len(SENTENCES),
        "total_paragraphs": len(PARAGRAPHS),
        "total_essays": len(ESSAYS),
        "total_items": len(SENTENCES) + len(PARAGRAPHS) + len(ESSAYS)
    }


if __name__ == "__main__":
    # Test nhanh
    summary = get_test_summary()
    print("📊 BỘ TEST DATA CHO VIETNAMESE TEXT CORRECTOR")
    print("=" * 50)
    print(f"📝 Số câu đơn: {summary['total_sentences']}")
    print(f"📄 Số đoạn văn: {summary['total_paragraphs']}")
    print(f"📚 Số bài văn: {summary['total_essays']}")
    print(f"📦 Tổng cộng: {summary['total_items']} items")
    print("=" * 50)
    
    # In ví dụ
    print("\n🔍 VÍ DỤ:")
    print("-" * 50)
    print("📥 Input:", SENTENCES[0]["input"])
    print("📤 Expected:", SENTENCES[0]["expected"])
