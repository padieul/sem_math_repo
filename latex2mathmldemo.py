
import latex2mathml.converter


if __name__ == "__main__":

    latex_input = "\sqrt{2}"
    mathml_output = latex2mathml.converter.convert(latex_input)
    print(mathml_output)