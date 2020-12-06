class Question:
    def __init__(self, num):
        self.num = num
        self.answers = []
        self.options = []
        self.text = None

    def setText(self, txt):
        self.text = txt

    def addOption(self, option):
        self.options.append(option)

    def addAnswer(self, answer):
        self.answers.append(answer)

    def iscorrect(self, answer):
        return answer in self.answers

def read(file_path):
    count = 1
    questions = []
    currentQuestion = None
    inText = False
    inOpt = False
    text = None
    opt = None
    with open(file_path, 'r') as file:
        line = file.readline()
        while line:
            if line.startswith("Question"):
                currentQuestion = Question(count)
                questions.append(currentQuestion)
                count = count + 1
                inText = True
                inOpt = False
                text = ""
            elif line.startswith("- "):
                if currentQuestion != None:
                    if text != None:
                        currentQuestion.setText(text)
                    if opt != None:
                        currentQuestion.addOption(opt)

                    opt = line[2:]
                    inOpt = True
                    inText = False
                    text = None
            elif line.startswith("Correct Answer: "):
                if opt != None:
                    currentQuestion.addOption(opt)
                opt = None
                inOpt = False
                answers = line[16:]
                for ans in answers:
                    currentQuestion.addAnswer(ans)
                currentQuestion = None
            else:
                if currentQuestion != None:
                    if inText == True:
                        text += line
                    if inOpt == True:
                        opt += line
            line = file.readline()
    return questions


if __name__ == '__main__':
    import sys
    file_path = sys.argv[1]
    questions = read(file_path)

    for q in questions:
        print(q.text)
        for o in q.options:
            print(o)
        print("Answer: ")
        for a in q.answers:
            print(a)