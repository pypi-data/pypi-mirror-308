from enum import StrEnum


class Runners(StrEnum):
    ECS = "ECS"
    Lambda = "LAMBDA"
    LambdaFemm = "LAMBDA_FEMM"
    LambdaGmsh = "LAMBDA_GMSH"
