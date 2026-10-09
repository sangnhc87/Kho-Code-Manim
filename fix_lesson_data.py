import re

for i in [22, 23, 24, 25]:
    path = f"Series-Dai-So-To-Hop/comb{i}_lesson_data.py"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        continue
    
    # We want to replace inside FORMULAS dictionary or the text
    # But wait, we can just safely replace the exact strings we know are failing.
    
    # 22
    content = content.replace("dp_(t+1,q)=sum_(p to q)dp_(t,p)", '"dp"_(t+1,q)=sum_(p -> q)"dp"_(t,p)')
    content = content.replace('dp_("mask"+2^j) += dp_("mask")', '"dp"_("mask"+2^j) += "dp"_("mask")')
    content = content.replace('dp_(mask+2^j) += dp_(mask)', '"dp"_("mask"+2^j) += "dp"_("mask")')
    content = content.replace('dp[0000]', '"dp"[0000]')
    content = content.replace('dp[1111]', '"dp"[1111]')
    content = content.replace('dp[i,k,q]', '"dp"[i,k,q]')
    content = content.replace('dp[i+1,k,q_0]+=dp[i,k,q]', '"dp"[i+1,k,q_0]+="dp"[i,k,q]')
    content = content.replace('dp[i+1,k+1,q_1]+=dp[i,k,q]', '"dp"[i+1,k+1,q_1]+="dp"[i,k,q]')
    content = content.replace('N=sum_q dp_(10,4,q,0)', 'N=sum_q "dp"_(10,4,q,0)')
    content = content.replace('0 <= mask < 2^4', '0 <= "mask" < 2^4')
    
    # 23
    content = content.replace('N(E_(i_1) cap dots cap E_(i_k))', 'N(E_(i_1) sect ... sect E_(i_k))')
    content = content.replace('6!-3 cdot 5!', '6!-3 dot.c 5!')
    content = content.replace('6!-3 cdot 5!+3 cdot 4!', '6!-3 dot.c 5!+3 dot.c 4!')
    content = content.replace('C_2^5 D_3=10 cdot 2=20', 'C_2^5 D_3=10 dot.c 2=20')
    content = content.replace('R_B(x)=R_(B-p)(x)+xR_(B-r-c)(x)', 'R_B(x)=R_(B-p)(x)+x R_(B-r-c)(x)')
    content = content.replace('xR_(B-r-c)(x)', 'x R_(B-r-c)(x)')
    content = content.replace('R_empty(x)=1', 'R_emptyset(x)=1')

    # 24 and 25 wait, what were the errors for them?
    # dyck_2 in 24.
    # burnside_2 in 25: "Fix(g)"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced strings in lesson_data")
