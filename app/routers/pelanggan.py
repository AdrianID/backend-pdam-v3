from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import pelanggan as pelanggan_crud
from app.crud import user as user_crud
from app.schemas.pelanggan import PelangganCreate
from app.utils.response_handler import create_response
from app.utils.dependencies import get_current_active_user, get_current_user
from app.models.user import User
from app.models.pelanggan import StatusPelanggan

router = APIRouter()

@router.post("/pengajuan-meteran")
async def create_pelanggan(
    *,
    db: Session = Depends(get_db),
    data: dict,  # Menggunakan dict untuk menerima data mentah
) -> Any:
    """
    Create new pelanggan and update user's pelanggan_id
    """
    try:
        # Validate user_id
        user = user_crud.get_user_by_id(db, id=data.get('user_id'))
        if not user:
            return create_response(
                status=False,
                message="User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Generate nomor pelanggan dan nomor meteran
        from datetime import datetime
        current_time = datetime.now()
        nomor_pelanggan = f"PLG{current_time.strftime('%Y%m%d%H%M%S%f')}"
        nomor_meteran = f"MTR{current_time.strftime('%Y%m%d%H%M%S%f')}"

        # Prepare pelanggan data
        pelanggan_data = {
            'kecamatan_id': data.get('kecamatan_id'),
            'desa_id': data.get('desa_id'),
            'kategori_id': data.get('kategori_id'),
            'area_distrik_id': data.get('area_distrik_id'),
            'sub_area_distrik_id': data.get('sub_area_distrik_id'),
            'jenis_pelanggan': 'regular',  # atau bisa disesuaikan dari input
            'nomor_pelanggan': nomor_pelanggan,
            'nomor_meteran': nomor_meteran,
            'nomor_kk': data.get('nomor_kk'),
            'nomor_sertifikat': data.get('nomor_sertifikat'),
            'nomor_telp': data.get('nomor_telp'),
            'nama_pelanggan': data.get('nama_pelanggan'),
            'nik': data.get('nik'),
            'alamat': data.get('alamat'),
            'rt': data.get('rt'),
            'rw': data.get('rw'),
            'nomor_rumah': data.get('nomor_rumah'),
            'gang': data.get('gang'),
            'blok': data.get('blok'),
            'luas_bangunan': float(data.get('luas_bangunan', 0)),
            'jenis_hunian': data.get('jenis_hunian'),
            'kebutuhan_air_awal': int(data.get('kebutuhan_air_awal', 0)),
            'kran_diminta': int(data.get('kran_diminta', 0)),
            'kwh_pln': data.get('kwh_pln'),
            'status_kepemilikan': data.get('status_kepemilikan'),
            'pekerjaan': data.get('pekerjaan'),
            'status': 'pending'
        }
        print("Status before schema:", pelanggan_data['status'])
        
        pelanggan_schema = PelangganCreate(**pelanggan_data)
        print("Status after schema:", pelanggan_schema.status)
        
        new_pelanggan = pelanggan_crud.create_pelanggan(db, pelanggan_schema)
        print("Status in new pelanggan:", new_pelanggan.status)

        # Update user's pelanggan_id
        user_update = {"pelanggan_id": new_pelanggan.id}
        updated_user = user_crud.update_user(db, db_user=user, user_in=user_update)

        return create_response(
            status=True,
            message="Pelanggan created successfully",
            data={
                "pelanggan": {
                    "id": new_pelanggan.id,
                    "nomor_pelanggan": new_pelanggan.nomor_pelanggan,
                    "nomor_meteran": new_pelanggan.nomor_meteran,
                    "nama_pelanggan": new_pelanggan.nama_pelanggan,
                    "status": new_pelanggan.status,
                    "created_at": new_pelanggan.created_at
                },
                "user": {
                    "id": updated_user.id,
                    "username": updated_user.username,
                    "email": updated_user.email,
                    "pelanggan_id": updated_user.pelanggan_id
                }
            },
            status_code=status.HTTP_201_CREATED
        )

    except ValueError as ve:
        return create_response(
            status=False,
            message=f"Validation error: {str(ve)}",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return create_response(
            status=False,
            message=f"Error creating pelanggan: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/pelanggan/status", response_model=None)
async def get_pelanggan_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get pelanggan status for current logged in user
    """
    try:
        # Get pelanggan data based on user's pelanggan_id
        if not current_user.pelanggan_id:
            return create_response(
                status=False,
                message="No pelanggan data found for this user",
                status_code=status.HTTP_404_NOT_FOUND
            )

        pelanggan = pelanggan_crud.get_pelanggan(db, current_user.pelanggan_id)
        if not pelanggan:
            return create_response(
                status=False,
                message="Pelanggan data not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return create_response(
            status=True,
            message="Pelanggan status retrieved successfully",
            data={
                "pelanggan": {
                    "id": pelanggan.id,
                    "nomor_pelanggan": pelanggan.nomor_pelanggan,
                    "nama_pelanggan": pelanggan.nama_pelanggan,
                    "status": pelanggan.status,
                    "created_at": pelanggan.created_at
                },
                "user": {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email
                }
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return create_response(
            status=False,
            message=f"Error retrieving pelanggan status: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/pelanggan/my-status", response_model=None)
async def get_my_pelanggan_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user's pelanggan status
    """
    try:
        # Get pelanggan data based on user's pelanggan_id
        if not current_user.pelanggan_id:
            return create_response(
                status=False,
                message="Anda belum terdaftar sebagai pelanggan",
                status_code=status.HTTP_404_NOT_FOUND
            )

        pelanggan = pelanggan_crud.get_pelanggan(db, current_user.pelanggan_id)
        if not pelanggan:
            return create_response(
                status=False,
                message="Data pelanggan tidak ditemukan",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return create_response(
            status=True,
            message="Status pelanggan berhasil diambil",
            data={
                "status": pelanggan.status,
                "nomor_pelanggan": pelanggan.nomor_pelanggan,
                "nama_pelanggan": pelanggan.nama_pelanggan
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return create_response(
            status=False,
            message=f"Error mengambil status pelanggan: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 