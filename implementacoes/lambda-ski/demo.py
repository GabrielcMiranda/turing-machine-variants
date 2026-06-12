# implementacoes/lambda-ski/demo.py
from ski import parse_ski, reduce_ski

def run_and_print_demo(title, expression_str, max_steps=100):
    print(f"\n--- {title} ---")
    print(f"Expressão Inicial: {expression_str}")
    term = parse_ski(expression_str)
    final_term, history = reduce_ski(term, max_steps)
    
    for idx, (term_str, rule) in enumerate(history, 1):
        print(f"  Passo {idx:02d}: {term_str}   ====> [{rule}]")
    
    print(f"Forma Normal Final: {final_term}")
    print(f"Total de passos: {len(history)}")
    if len(history) == max_steps:
        print("⚠️ Limite de passos atingido (Possível divergência/loop infinito).")

if __name__ == "__main__":
    print("==================================================")
    print("      DEMONSTRAÇÃO SISTEMA COMBINADORES SKI       ")
    print("==================================================")

    # 1. Identidade Equivalente (I = SKK)
    run_and_print_demo("1. Identidade como SKK (SKK x)", "S K K x")

    # 2. Booleanos de Church (TRUE = K, FALSE = K I)
    run_and_print_demo("2. Booleano TRUE escolhendo o primeiro operando (K a b)", "K a b")

    # 3. Numeral de Church 2 em SKI: 2 = S (S (K S) K) (S K K) = S B I.
    # Aplicado a f e x, reduz a f (f x) ("aplique f duas vezes") em 7 passos.
    run_and_print_demo("3. Numeral de Church 2 aplicado a f x (>= 7 passos)", "S (S (K S) K) (S K K) f x")

    # 4. Termo que não normaliza (Loop Infinito controlado)
    # Omega = S I I (S I I) -> se auto-replica infinitamente
    run_and_print_demo("4. Loop de Parada Infinito (Omega)", "S I I (S I I)", max_steps=5)