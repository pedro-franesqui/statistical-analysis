import summary_stats as st
import probability_calc as prob

def main():
    src = "P(A) = p(¬C ∩ D) + P(A u ¬B) - P(E)"
    parser = prob.ProbabilityParser(src)
    parser.expr_eval()

if __name__ == "__main__":
    main()