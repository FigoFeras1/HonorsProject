from operations import get_min
import time
import operations

def test_get_min(arr, col):
	start_time = time.perf_counter()
	get_min(arr, col)
	end_time = time.perf_counter()
	print(f"Time for get_min using {col=}: {end_time-start_time=}")