import src.aocs_lab.sun_time as sun_time
import numpy as np

if __name__ == "__main__":
    # 太阳矢量与轨道面法线夹角
    beta_angle = np.deg2rad(31)
    sun_time.sun_time(beta_angle, 6900e3)

    beta_angle = np.deg2rad(67)
    sun_time.sun_time(beta_angle, 6900e3)