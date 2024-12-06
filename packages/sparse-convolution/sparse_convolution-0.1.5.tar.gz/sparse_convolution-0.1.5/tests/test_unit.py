import traceback
import time

import numpy as np
import scipy.signal

from sparse_convolution import Toeplitz_convolution2d

def test_toeplitz_convolution2d():
    """
    Test toeplitz_convolution2d
    Tests for modes, shapes, values, and for sparse matrices against
     scipy.signal.convolve2d.

    RH 2022
    """
    ## test toepltiz convolution

    print(f'testing with batching=False')

    stt = shapes_to_try = np.meshgrid(np.arange(1, 7), np.arange(1, 7), np.arange(1, 7), np.arange(1, 7))
    stt = [s.reshape(-1) for s in stt]

    for mode in ['full', 'same', 'valid']:
        for ii in range(len(stt[0])):
            x = np.random.rand(stt[0][ii], stt[1][ii])
            k = np.random.rand(stt[2][ii], stt[3][ii])
    #         print(stt[0][ii], stt[1][ii], stt[2][ii], stt[3][ii])

            try:
                t = Toeplitz_convolution2d(x_shape=x.shape, k=k, mode=mode, dtype=None)
                out_t2d = t(x, batching=False, mode=mode)
                out_t2d_s = t(scipy.sparse.csr_matrix(x), batching=False, mode=mode)
                out_sp = scipy.signal.convolve2d(x, k, mode=mode)
            except Exception as e:
                if mode == 'valid' and (stt[0][ii] < stt[2][ii] or stt[1][ii] < stt[3][ii]):
                    if 'x must be larger than k' in str(e):
                        continue
                print(f'A) test failed with shapes:  x: {x.shape}, k: {k.shape} and mode: {mode} and Exception: {e}  {traceback.format_exc()}')
                success = False
                break
            try:
                if np.allclose(out_t2d, out_t2d_s.toarray()) and np.allclose(out_t2d, out_sp) and np.allclose(out_sp, out_t2d_s.toarray()):
                    success = True
                    continue
            except Exception as e:
                print(f'B) test failed with shapes:  x: {x.shape}, k: {k.shape} and mode: {mode} and Exception: {e}  {traceback.format_exc()}')
                success = False
                break

            else:
                print(f'C) test failed with batching==False, shapes:  x: {x.shape}, k: {k.shape} and mode: {mode}')
                success = False
                break       

    print(f'testing with batching=True')

    for mode in ['full', 'same', 'valid']:
        for ii in range(len(stt[0])):
            x = np.stack([np.random.rand(stt[0][ii], stt[1][ii]).reshape(-1) for jj in range(3)], axis=0)
            k = np.random.rand(stt[2][ii], stt[3][ii])
    #         print(stt[0][ii], stt[1][ii], stt[2][ii], stt[3][ii])

            try:
                t = Toeplitz_convolution2d(x_shape=(stt[0][ii], stt[1][ii]), k=k, mode=mode, dtype=None)
                out_sp = np.stack([scipy.signal.convolve2d(x_i.reshape(stt[0][ii], stt[1][ii]), k, mode=mode) for x_i in x], axis=0)
                out_t2d = t(x, batching=True, mode=mode).reshape(3, out_sp.shape[1], out_sp.shape[2])
                out_t2d_s = t(scipy.sparse.csr_matrix(x), batching=True, mode=mode).toarray().reshape(3, out_sp.shape[1], out_sp.shape[2])
            except Exception as e:
                if mode == 'valid' and (stt[0][ii] < stt[2][ii] or stt[1][ii] < stt[3][ii]):
                    if 'x must be larger than k' in str(e):
                        continue
                else:
                    print(f'A) test failed with shapes:  x: {x.shape}, k: {k.shape} and mode: {mode} and Exception: {e}  {traceback.format_exc()}')
                success = False
                break
            try:
                if np.allclose(out_t2d, out_t2d_s) and np.allclose(out_t2d, out_sp) and np.allclose(out_sp, out_t2d_s):
                    success = True
                    continue
            except Exception as e:
                print(f'B) test failed with shapes:  x: {x.shape}, k: {k.shape} and mode: {mode} and Exception: {e}  {traceback.format_exc()}')
                success = False
                break

            else:
                print(f'C) test failed with batching==False, shapes:  x: {x.shape}, k: {k.shape} and mode: {mode}')
                print(f"Failure analysis: \n")
                print(f"Shapes: x: {x.shape}, k: {k.shape}, out_t2d: {out_t2d.shape}, out_t2d_s: {out_t2d_s.shape}, out_sp: {out_sp.shape}")
                print(f"out_t2d: {out_t2d}")
                print(f"out_t2d_s: {out_t2d_s}")
                print(f"out_sp: {out_sp}")

                success = False
                break           
    print(f'success with all shapes and modes') if success else None
    assert success, 'test failed'
    # return success