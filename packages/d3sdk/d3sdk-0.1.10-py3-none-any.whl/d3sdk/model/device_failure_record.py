from typing import List

class Fm:
    def __init__(self, fm_code, fm_name):
        self.fm_code = fm_code
        self.fm_name = fm_name

    def __repr__(self):
        return f"Fm(fm_code={self.fm_code}, fm_name={self.fm_name})"

class DeviceFailureRecord:
    def __init__(self, dfem_code, display_name, dfem_bjlx, dfem_sxmsbh, description, dfem_bjs, dfem_bjdj, dfem_zt, dfem_gjz, dfem_zzbjsj, dfem_zxbjsj, device_code, fms:List[Fm]):
        self.dfem_code = dfem_code
        self.display_name = display_name
        self.dfem_bjlx = dfem_bjlx
        self.dfem_sxmsbh = dfem_sxmsbh
        self.description = description
        self.dfem_bjs = dfem_bjs
        self.dfem_bjdj = dfem_bjdj
        self.dfem_zt = dfem_zt
        self.dfem_gjz = dfem_gjz
        self.dfem_zzbjsj = dfem_zzbjsj
        self.dfem_zxbjsj = dfem_zxbjsj
        self.device_code = device_code
        self.fms = fms

    def __repr__(self):
        return (f"DeviceFailureRecord(dfem_code={self.dfem_code}, "
                f"display_name={self.display_name}, "
                f"dfem_bjlx={self.dfem_bjlx}, "
                f"dfem_sxmsbh={self.dfem_sxmsbh}, "
                f"description={self.description}, "
                f"dfem_bjs={self.dfem_bjs}, "
                f"dfem_bjdj={self.dfem_bjdj}, "
                f"dfem_zt={self.dfem_zt}, "
                f"dfem_gjz={self.dfem_gjz}, "
                f"dfem_zzbjsj={self.dfem_zzbjsj}, "
                f"dfem_zxbjsj={self.dfem_zxbjsj}, "
                f"device_code={self.device_code}, "
                f"fms={self.fms!r})")


    # @staticmethod
    # def from_row(row):
    #     return DeviceFailureRecord(
    #         dfem_code=row['dfem_code'],
    #         display_name=row['display_name'],
    #         dfem_bjlx=row['dfem_bjlx'],
    #         dfem_sxmsbh=row['dfem_sxmsbh'],
    #         description=row['description'],
    #         dfem_bjs=row['dfem_bjs'],
    #         dfem_bjdj=row['dfem_bjdj'],
    #         dfem_zt=row['dfem_zt'],
    #         dfem_gjz=row['dfem_gjz'],
    #         dfem_zzbjsj=row['dfem_zzbjsj'],
    #         dfem_zxbjsj=row['dfem_zxbjsj'],
    #         device_code=row['device_code'],
    #         fm_code=row['fm_code'],
    #         fm_name=row['fm_name']
    #     )


# # 创建示例对象
# record1 = DeviceFailureRecord(
#     "AG0000121409",
#     "12号定子线棒层间温度运行值持续动态超限",
#     "failure",
#     "FM800412",
#     "12号定子线棒层间温度运行值持续动态超限",
#     4,
#     "注意",
#     "已查看",
#     "定子绕组温度，动态预警",
#     "2024-06-30 12:56:48",
#     "2024-06-30 13:59:48",
#     "T0000000002",
#     "QLJ00001",
#     "定子"
# )
#
# # 打印对象
# print(record1)