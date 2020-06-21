from django.db import models
from profile.models import TimestampedModel

class Status(TimestampedModel):

    #url cua post
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    #profile tao status
    author = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='statuses')
    title = models.CharField(max_length = 100)
    image = models.URLField(blank=True, null=True)
    content = models.TextField()

    location_choice = [('An Giang', 'An Giang'), ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'), ('Bắc Giang', 'Bắc Giang'), ('Bắc Kạn', 'Bắc Kạn'), 
    ('Bạc Liêu', 'Bạc Liêu'), ('Bắc Ninh', 'Bắc Ninh'), ('Bến Tre', 'Bến Tre'), ('Bình Định', 'Bình Định'), ('Bình Dương', 'Bình Dương'), 
    ('Bình Phước', 'Bình Phước'), ('Bình Thuận', 'Bình Thuận'), ('Cà Mau', 'Cà Mau'), ('Cao Bằng', 'Cao Bằng'), ('Đắk Lắk', 'Đắk Lắk'), 
    ('Đắk Nông', 'Đắk Nông'), ('Điện Biên', 'Điện Biên'), ('Đồng Nai', 'Đồng Nai'), ('Đồng Tháp', 'Đồng Tháp'), ('Gia Lai', 'Gia Lai'), 
    ('Hà Giang', 'Hà Giang'),('Hà Nam', 'Hà Nam'), ('Hà Tĩnh', 'Hà Tĩnh'), ('Hải Dương', 'Hải Dương'), ('Hậu Giang', 'Hậu Giang'), 
    ('Hòa Bình', 'Hòa Bình'), ('Hưng Yên', 'Hưng Yên'), ('Khánh Hòa', 'Khánh Hòa'), ('Kiên Giang', 'Kiên Giang'), ('Kon Tum', 'Kon Tum'), 
    ('Lai Châu', 'Lai Châu'), ('Lâm Đồng', 'Lâm Đồng'), ('Lạng Sơn', 'Lạng Sơn'), ('Lào Cai', 'Lào Cai'), ('Long An', 'Long An'), 
    ('Nam Định', 'Nam Định'), ('Nghệ An', 'Nghệ An'), ('Ninh Bình', 'Ninh Bình'), ('Ninh Thuận', 'Ninh Thuận'), ('Phú Thọ', 'Phú Thọ'), 
    ('Quảng Bình', 'Quảng Bình'),('Quảng Nam', 'Quảng Nam'), ('Quảng Ngãi', 'Quảng Ngãi'), ('Quảng Ninh', 'Quảng Ninh'), ('Quảng Trị', 'Quảng Trị'), 
    ('Sóc Trăng', 'Sóc Trăng'), ('Sơn La', 'Sơn La'), ('Tây Ninh', 'Tây Ninh'), ('Thái Bình', 'Thái Bình'), ('Thái Nguyên', 'Thái Nguyên'), 
    ('Thanh Hóa', 'Thanh Hóa'), ('Thừa Thiên Huế', 'Thừa Thiên Huế'), ('Tiền Giang', 'Tiền Giang'), ('Trà Vinh', 'Trà Vinh'), 
    ('Tuyên Quang', 'Tuyên Quang'), ('Vĩnh Long', 'Vĩnh Long'), ('Vĩnh Phúc', 'Vĩnh Phúc'), ('Yên Bái', 'Yên Bái'), ('Phú Yên', 'Phú Yên'),
    ('Cần Thơ', 'Cần Thơ'), ('Đà Nẵng', 'Đà Nẵng'), ('Hải Phòng', 'Hải Phòng'), ('Hà Nội', 'Hà Nội'), ('TP HCM', 'TP HCM'),]
    
    loaction = models.CharField(max_length=30, choices=location_choice, default='An Giang')
    
    def __str__(self):
        return (self.title, self.content)



class Comment(TimestampedModel):
    body = models.TextField()

    status = models.ForeignKey(
        'status.Status', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'profile.Profile', related_name='comments', on_delete=models.CASCADE
    )