"""
Database models module
"""

from app.models.kecamatan import Kecamatan
from app.models.desa import Desa
from app.models.area import Area
from app.models.area_distrik import AreaDistrik
from app.models.sub_area_distrik import SubAreaDistrik
from app.models.kategori import Kategori
from app.models.jabatan import Jabatan
from app.models.pegawai import Pegawai
from app.models.pelanggan import Pelanggan
from app.models.spks import SPKS
from app.models.gelombang_spks import GelombangSPKS
from app.models.iku import IKU
from app.models.penggunaan_air import PenggunaanAir
from app.models.role import Role
from app.models.tempat import Tempat
from app.models.user import User
from app.models.tanggungan import Tanggungan

# Ini memastikan semua model di-load sebelum SQLAlchemy membuat relationships 