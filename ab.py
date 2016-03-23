#!/usr/bin/env python
# coding=utf-8
import argparse
from concurrent.futures import as_completed, ThreadPoolExecutor
import time

import requests
import requests.exceptions


def prep_args():
    parser = argparse.ArgumentParser(
        description='A simple HTTP server benchmarking tool')
    parser.add_argument('-n', type=int, help='number of requests')
    parser.add_argument('-c', type=int, nargs='?', help='concurrency')
    parser.add_argument('url', help='url')
    args = parser.parse_args()
    url = args.url
    requests_num = args.n
    concurrency = args.c
    return url, requests_num, concurrency


def load_url(url, timeout=5):
    start_time = time.time()
    try:
        requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        return None
    return (time.time() - start_time) * 1000


def benchmark(url, requests_num, concurrency=None):
    if not concurrency:
        concurrency = 1
    results = []
    failed_num = 0
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(load_url, url) for i in range(requests_num)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(future.result())
            else:
                failed_num += 1
    results.sort()
    print('''
          Concurrency level: {}
          Complete requests: {}
          Failed requests: {}
          Requests per second: {:g}

          Connection Times (ms)
                   min  max
          Connect: {:g}   {:g}
          '''.format(
              concurrency, requests_num, failed_num, sum(results)/len(results),
              results[0], results[-1]
              ))


if __name__ == '__main__':
    benchmark(*prep_args())
