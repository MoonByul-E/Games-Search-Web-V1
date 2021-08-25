test = {
    1: {"name": "가", "score": 100},
    2: {"name": "나", "score": 10}
}

for key, value in test.items():
    for key1, value1 in value.items():
        print(f"{key}: {key1} - {value1}")
    print("=================")