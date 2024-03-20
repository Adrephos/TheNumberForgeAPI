package utils

import (
	"errors"
	"github.com/Pramod-Devireddy/go-exprtk"
)

func EvalParameter(s string) (float64, error) {
	expression := exprtk.NewExprtk()
	defer expression.Delete()
	expression.SetExpression(s)

	err := expression.CompileExpression()
	if err != nil || s == "" {
		return 0, errors.New("please enter a valid expression")
	}

	return expression.GetEvaluatedValue(), nil
}
