.data
label_0_0: .double 0.0
label_1_0: .double 1.0
label_3: .double 3
label_4: .double 4
label_10: .double 10
label_2: .double 2
label_2_5: .double 2.5
label_5: .double 5
label_8: .double 8
label_5_5: .double 5.5
label_1: .double 1
label_MEM: .double 0.0
current_line: .word 0
results: .space 80
stack_base: .space 4096
stack_top: .word 0

.text
.global _start
_start:
ldr r0, =stack_base
ldr r1, =stack_top
str r0, [r1]
mov r0, #1
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_3
vldr d0, [r0]
bl push_d0
ldr r0, =label_4
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vadd.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #0
vstr d0, [r0]

mov r0, #2
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_10
vldr d0, [r0]
bl push_d0
ldr r0, =label_2
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vsub.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #8
vstr d0, [r0]

mov r0, #3
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_2_5
vldr d0, [r0]
bl push_d0
ldr r0, =label_5
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vmul.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #16
vstr d0, [r0]

mov r0, #4
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_8
vldr d0, [r0]
bl push_d0
ldr r0, =label_2
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vdiv.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #24
vstr d0, [r0]

mov r0, #5
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_10
vldr d0, [r0]
bl push_d0
ldr r0, =label_3
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
bl op_int_div
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #32
vstr d0, [r0]

mov r0, #6
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_10
vldr d0, [r0]
bl push_d0
ldr r0, =label_3
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
bl op_int_mod
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #40
vstr d0, [r0]

mov r0, #7
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_2
vldr d0, [r0]
bl push_d0
ldr r0, =label_3
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
bl op_pow
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #48
vstr d0, [r0]

mov r0, #8
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_MEM
vldr d0, [r0]
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #56
vstr d0, [r0]

mov r0, #9
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_5_5
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vadd.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #64
vstr d0, [r0]

mov r0, #10
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_15_0
vldr d0, [r0]
bl push_d0
ldr r0, =label_5
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vsub.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #8
vstr d0, [r0]

mov r0, #3
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_6
vldr d0, [r0]
bl push_d0
ldr r0, =label_2
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vmul.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #16
vstr d0, [r0]

mov r0, #4
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_9
vldr d0, [r0]
bl push_d0
ldr r0, =label_3
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vdiv.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #24
vstr d0, [r0]

mov r0, #5
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_12
vldr d0, [r0]
bl push_d0
ldr r0, =label_4
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
bl op_int_div
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #32
vstr d0, [r0]

mov r0, #6
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_14
vldr d0, [r0]
bl push_d0
ldr r0, =label_5
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
bl op_int_mod
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #40
vstr d0, [r0]

mov r0, #7
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_3
vldr d0, [r0]
bl push_d0
ldr r0, =label_2
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
bl op_pow
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #48
vstr d0, [r0]

mov r0, #8
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_10_0
vldr d0, [r0]
bl push_d0
bl pop_to_d0
ldr r0, =label_VAR
vstr d0, [r0]
bl push_d0
ldr r0, =label_10
vldr d0, [r0]
bl push_d0
ldr r0, =label_20
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vadd.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #56
vstr d0, [r0]

mov r0, #9
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_VAR
vldr d0, [r0]
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #64
vstr d0, [r0]

mov r0, #10
ldr r1, =current_line
str r0, [r1]
ldr r0, =label_1
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl res_lookup
bl push_d0
ldr r0, =label_1_5
vldr d0, [r0]
bl push_d0
ldr r0, =label_2
vldr d0, [r0]
bl push_d0
bl pop_to_d0
bl pop_to_d1
vadd.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
bl pop_to_d1
vadd.f64 d0, d1, d0
bl push_d0
bl pop_to_d0
ldr r0, =results
add r0, r0, #72
vstr d0, [r0]


b end

push_d0:
push {r0, r1}
ldr r0, =stack_top
ldr r1, [r0]
vstr d0, [r1]
add r1, r1, #8
str r1, [r0]
pop {r0, r1}
bx lr

pop_to_d0:
push {r0, r1}
ldr r0, =stack_top
ldr r1, [r0]
sub r1, r1, #8
vldr d0, [r1]
str r1, [r0]
pop {r0, r1}
bx lr

pop_to_d1:
push {r0, r1}
ldr r0, =stack_top
ldr r1, [r0]
sub r1, r1, #8
vldr d1, [r1]
str r1, [r0]
pop {r0, r1}
bx lr

res_lookup:
ldr r0, =current_line
ldr r1, [r0]
vcvt.s32.f64 s0, d0
vmov r2, s0
sub r1, r1, r2
sub r1, r1, #1
cmp r1, #0
blt res_zero
mov r2, #8
mul r1, r1, r2
ldr r0, =results
add r0, r0, r1
vldr d0, [r0]
bx lr
res_zero:
ldr r0, =label_0_0
vldr d0, [r0]
bx lr

op_int_div:
vcvt.s32.f64 s0, d1
vcvt.s32.f64 s2, d0
vmov r0, s0
vmov r1, s2
cmp r1, #0
beq int_div_zero
mov r2, #0
mov r3, r0
int_div_loop:
cmp r3, r1
blt int_div_done
sub r3, r3, r1
add r2, r2, #1
b int_div_loop
int_div_done:
vmov s4, r2
vcvt.f64.s32 d0, s4
bx lr
int_div_zero:
ldr r0, =label_0_0
vldr d0, [r0]
bx lr

op_int_mod:
vcvt.s32.f64 s0, d1
vcvt.s32.f64 s2, d0
vmov r0, s0
vmov r1, s2
cmp r1, #0
beq int_mod_zero
mov r2, r0
int_mod_loop:
cmp r2, r1
blt int_mod_done
sub r2, r2, r1
b int_mod_loop
int_mod_done:
vmov s4, r2
vcvt.f64.s32 d0, s4
bx lr
int_mod_zero:
ldr r0, =label_0_0
vldr d0, [r0]
bx lr

op_pow:
push {r0, r1}
vcvt.s32.f64 s0, d0
vmov r1, s0
ldr r0, =label_1_0
vldr d0, [r0]
cmp r1, #0
beq pow_done
pow_loop:
vmul.f64 d0, d0, d1
subs r1, r1, #1
bne pow_loop
pow_done:
pop {r0, r1}
bx lr

end:
b end