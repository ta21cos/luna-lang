import sys
from converter import Inst, convert_bf_to_instruction, convert_luna_to_brainfxck


class Pointer:
    def __init__(self):
        self.__p = 0

    def inc(self):
        self.__p += 1

    def dec(self):
        self.__p -= 1
        # 負になるかも

    def set(self, v):
        self.__p = v

    def __call__(self):
        return self.__p


class Interpreter:
    def __init__(self):
        self.memory = [0 for _ in range(100)]

    def inc(self, p):
        self.memory[p()] += 1

    def dec(self, p):
        self.memory[p()] -= 1

    def out(self, p):
        return self.memory[p()]

    def inp(self, p, v):
        self.memory[p()] = v

    def jmpifz(self, p, insts, a):
        if self.memory[p()] == 0:
            _i = self.next_ret_index(insts, a)
            a.set(_i)

    def retifnz(self, p, insts, a):
        if self.memory[p()] != 0:
            _i = self.prev_jmp_index(insts, a)
            a.set(_i)

    def next_ret_index(self, insts, a):
        count = 0  # for nest
        for i in range(a()+1, len(insts)):
            if insts[i] == Inst.JMPIFZ:
                count += 1
            elif insts[i] == Inst.RETIFNZ:
                if count == 0:
                    return i
                else:
                    count -= 1
        print('could not jump')
        return len(insts)

    def prev_jmp_index(self, insts, a):
        count = 0
        for i in range(0, a()-1)[::-1]:
            if insts[i] == Inst.RETIFNZ:
                count += 1
            if insts[i] == Inst.JMPIFZ:
                if count == 0:
                    return i
                else:
                    count -= 1
        print('could not return')
        return len(insts)


execute_dict = {
    Inst.INCP: lambda intp, p, insts, a: p.inc(),
    Inst.DECP: lambda intp, p, insts, a: p.dec(),
    Inst.INCV: lambda intp, p, insts, a: intp.inc(p),
    Inst.DECV: lambda intp, p, insts, a: intp.dec(p),
    Inst.OUTV: lambda intp, p, insts, a: print(chr(intp.out(p)), end=''),
    Inst.INPV: lambda intp, p, insts, a: intp.inp(p, ord(input())),
    Inst.JMPIFZ: lambda intp, p, insts, a: intp.jmpifz(p, insts, a),
    Inst.RETIFNZ: lambda intp, p, insts, a: intp.retifnz(p, insts, a)
}


def execute(instructions):
    addr = Pointer()  # 現在実行している命令を示すポインタ，ほぼ同じデータ構造なので流用
    p = Pointer()  # 現在参照しているメモリを表すデータポインタ
    interpreter = Interpreter()

    while addr() < len(instructions):
        try:
            execution = execute_dict[instructions[addr()]]
            execution(interpreter, p, instructions, addr)
            addr.inc()
        except:
            print("Could not execute", sys.exc_info())
            break
    print()
    return


def main(filename):
    with open(filename) as f:
        input_luna = f.read()

    instructions = convert_luna_to_brainfxck(input_luna)
    execute(instructions)


# python interpreter.py luna.txtのように実行
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Filename is not found.')
        exit()
    filename = sys.argv[1]
    main(filename)
