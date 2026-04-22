import os
import numpy as np
from scipy.io import loadmat


class GNBG:
    def __init__(self, Dimension, CompNum, CompMinPos, CompSigma,
                 CompH, Mu, Omega, Lambda, RotationMatrix):
        self.Dimension = int(Dimension)
        self.CompNum = int(CompNum)
        self.CompMinPos = np.asarray(CompMinPos, dtype=float)
        self.CompSigma = np.asarray(CompSigma, dtype=float).reshape(-1)
        self.CompH = np.asarray(CompH, dtype=float)
        self.Mu = np.asarray(Mu, dtype=float)
        self.Omega = np.asarray(Omega, dtype=float)
        self.Lambda = np.asarray(Lambda, dtype=float).reshape(-1)
        self.RotationMatrix = np.asarray(RotationMatrix, dtype=float)

    def transform(self, X, Alpha, Beta):
        X = np.asarray(X, dtype=float)
        Alpha = np.ravel(Alpha)
        Beta = np.ravel(Beta)

        Y = X.copy()

        tmp = X > 0
        Y[tmp] = np.log(X[tmp])
        Y[tmp] = np.exp(
            Y[tmp] + Alpha[0] * (np.sin(Beta[0] * Y[tmp]) + np.sin(Beta[1] * Y[tmp]))
        )

        tmp = X < 0
        Y[tmp] = np.log(-X[tmp])
        Y[tmp] = -np.exp(
            Y[tmp] + Alpha[1] * (np.sin(Beta[2] * Y[tmp]) + np.sin(Beta[3] * Y[tmp]))
        )

        return Y

    def fitness(self, X):
        X = np.asarray(X, dtype=float).reshape(-1, 1)
        f = np.full(self.CompNum, np.nan)

        for k in range(self.CompNum):
            R = self.RotationMatrix[:, :, k] if self.RotationMatrix.ndim == 3 else self.RotationMatrix
            shift = self.CompMinPos[k, :].reshape(-1, 1)

            a = self.transform(
                (X - shift).T @ R.T,
                self.Mu[k, :],
                self.Omega[k, :],
            )
            b = self.transform(
                R @ (X - shift),
                self.Mu[k, :],
                self.Omega[k, :],
            )

            quad = float(np.squeeze(a @ np.diag(np.ravel(self.CompH[k, :])) @ b))
            sigma_k = float(self.CompSigma[k])
            lambda_k = float(self.Lambda[k])

            f[k] = sigma_k + quad ** lambda_k

        return float(np.min(f))

    __call__ = fitness


def load_gnbg_instance(repo_dir, idx):
    data = loadmat(os.path.join(repo_dir, f"f{idx}.mat"))["GNBG"]

    def get_scalar(field):
        return np.array([item[0] for item in data[field].flatten()])[0, 0]

    return GNBG(
        Dimension=get_scalar("Dimension"),
        CompNum=get_scalar("o"),
        CompMinPos=np.array(data["Component_MinimumPosition"][0, 0], dtype=float),
        CompSigma=np.atleast_1d(np.array(data["ComponentSigma"][0, 0], dtype=float)).reshape(-1),
        CompH=np.array(data["Component_H"][0, 0], dtype=float),
        Mu=np.array(data["Mu"][0, 0], dtype=float),
        Omega=np.array(data["Omega"][0, 0], dtype=float),
        Lambda=np.atleast_1d(np.array(data["lambda"][0, 0], dtype=float)).reshape(-1),
        RotationMatrix=np.array(data["RotationMatrix"][0, 0], dtype=float),
    )