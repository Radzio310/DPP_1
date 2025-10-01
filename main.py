# file: main.py
def draw_mandelbrot(w=80, h=24, it=25):
    for y in range(h):
        for x in range(w):
            # rzutowanie pikseli terminala na płaszczyznę zespoloną
            c = complex((x - w/2)/(w/4), (y - h/2)/(h/4))
            z = 0
            j = 0
            while abs(z) <= 2 and j < it:
                z = z*z + c
                j += 1
            print(" .:-=+*#%@"[j*10//it], end="")
        print()

def main():
    draw_mandelbrot()  # możesz podać np. draw_mandelbrot(100, 30, 40)

if __name__ == "__main__":
    main()
