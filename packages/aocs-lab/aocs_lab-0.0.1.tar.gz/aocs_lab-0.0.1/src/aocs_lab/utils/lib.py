from math import sqrt, sin, cos, pi
from . import constants
import numpy as np

def latitude_to_angular_velocity(latitude):
    omega_north = constants.EARTH_ROTATION_RATE * cos(latitude)
    omega_up = constants.EARTH_ROTATION_RATE * sin(latitude)

    return omega_north, omega_up

def orbit_period(semimajor_axis):
    return sqrt( 4*pi**2 * semimajor_axis**3 / constants.GM_EARTH ) # Kepler's Third laws of planetary motion

def orbit_angular_rate(semimajor_axis):
    return 2*pi / orbit_period(semimajor_axis)

# https://en.wikipedia.org/wiki/Latitude#Latitude_on_the_ellipsoid



def orthogonality_error(A: np.array):
    """
    计算矩阵 A 的正交性误差，基于 Frobenius 范数的偏离度计算。
    """
    I = np.eye(A.shape[1])  # 单位矩阵
    error_matrix = A.T @ A - I  # 计算 A^T A 与 I 的差
    frobenius_norm = np.linalg.norm(error_matrix, 'fro')  # Frobenius 范数
    return frobenius_norm

def theta_deg_to_cos_matrix(theta_deg):
    theta_rad = np.deg2rad(theta_deg)
    A = np.cos(theta_rad)    
    return A

def vector_angle(v1, v2):
    dot_product = np.dot(v1, v2)

    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle = np.arccos(cos_theta)

    return angle