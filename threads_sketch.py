import time
import threading
import concurrent.futures


lock = threading.Lock()


def L1(trem: str) -> None:
    print(f"{trem}: passando no trilho L1")
    time.sleep(1)


def L2(trem: str) -> None:
    print(f"{trem}: passando no trilho L2")
    time.sleep(1)


def L3(trem: str) -> None:
    print(f"{trem}: passando no trilho L3")
    time.sleep(1)


def L4(trem: str) -> None:
    print(f"{trem}: passando no trilho L4")
    time.sleep(1)


def L5(trem: str) -> None:
    print(f"{trem}: passando no trilho L5")
    time.sleep(1)


def L6(trem: str) -> None:
    print(f"{trem}: passando no trilho L6")
    time.sleep(1)


def L7(trem: str) -> None:
    print(f"{trem}: passando no trilho L7")
    time.sleep(1)


def L8(trem: str) -> None:
    print(f"{trem}: passando no trilho L8")
    time.sleep(1)


def L9(trem: str) -> None:
    print(f"{trem}: passando no trilho L9")
    time.sleep(1)


def L10(trem: str) -> None:
    print(f"{trem}: passando no trilho L10")
    time.sleep(1)


def L3L4(trem: str) -> None:
    with lock:
        L3(trem)
        L4(trem)


def L6L3(trem: str) -> None:
    with lock:
        L6(trem)
        L3(trem)


def L4L6(trem: str) -> None:
    with lock:
        L4(trem)
        L6(trem)


def mover_trem(trem_id: str) -> None:
    percursos = {
        "verde": [L1, L2, L3L4],
        "roxo": [L5, L6L3, L7],
        "vermelho": [L8, L4L6, L9, L10],
    }
    percurso = percursos[trem_id]
    while True:
        for trilho in percurso:
            trilho(trem_id)


def mover_trens() -> None:
    while True:
        mover_trem("verde")
        mover_trem("roxo")
        mover_trem("vermelho")


if __name__ == "__main__":
    trens = ["verde", "roxo", "vermelho"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(mover_trem, trens)
