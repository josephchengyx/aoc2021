class ALU:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.error = False

    def __repr__(self):
        return f"w[{self.w}] x[{self.x}] y[{self.y}] z[{self.z}]"

    def _get_var(self, var):
        return getattr(self, var)

    def _set_var(self, var, val):
        setattr(self, var, val)

    def inp(self, arg1, arg2):
        self._set_var(arg1, arg2)

    def add(self, arg1, arg2):
        val1, val2 = self._get_var(arg1), arg2
        if isinstance(val2, str):
            val2 = self._get_var(val2)
        self._set_var(arg1, val1 + val2)

    def mul(self, arg1, arg2):
        val1, val2 = self._get_var(arg1), arg2
        if isinstance(val2, str):
            val2 = self._get_var(val2)
        self._set_var(arg1, val1 * val2)

    def div(self, arg1, arg2):
        val1, val2 = self._get_var(arg1), arg2
        if isinstance(val2, str):
            val2 = self._get_var(val2)
        if val2 == 0:
            self.error = True
            return
        self._set_var(arg1, val1 // val2)

    def mod(self, arg1, arg2):
        val1, val2 = self._get_var(arg1), arg2
        if isinstance(val2, str):
            val2 = self._get_var(val2)
        if val1 < 0 or val2 <= 0:
            self.error = True
            return
        self._set_var(arg1, val1 % val2)

    def eql(self, arg1, arg2):
        val1, val2 = self._get_var(arg1), arg2
        if isinstance(val2, str):
            val2 = self._get_var(val2)
        self._set_var(arg1, int(val1 == val2))

    def crashed(self):
        return self.error

    def reset(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.error = False

    def set_state(self, state):
        self.w, self.x, self.y, self.z = state
        self.error = False

    def run(self, instructions, argin):
        if not isinstance(argin, list):
            argin = [argin]
        i_in = 0
        for line in instructions:
            op = line[0]
            if op == "inp":
                if i_in >= len(argin):
                    return
                arg1, arg2 = line[1], argin[i_in]
                i_in += 1
            else:
                arg1, arg2 = line[1:]
            self._get_var(op)(arg1, arg2)
            if self.error:
                return

    def output(self):
        return self.w, self.x, self.y, self.z

    def disp(self):
        print(self)
