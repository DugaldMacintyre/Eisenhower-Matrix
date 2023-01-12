# Eisenhower matrix class structure
class Matrix(object):
    def __init__(self):
        self.matrix = [[{}, {}], [{}, {}]]
        self.done = []
        self.deletedTasks = {}

    # Prints the tasks in each quarter
    def printQuarter(self, important, urgent):
        for task, time in self.matrix[important][urgent].items():
            if time == 1:
                print(task + ": " + str(time) + " hour")
            else:
                print(task + ": " + str(time) + " hours")
        return

    # Inserts tasks to the matrix
    def insert(self, task, time, important, urgent):
        # Although counterintuitive, this means that items are not important or urgent. Therefore, don't need to be done
        if important == True and urgent == True:
            self.deletedTasks[task] = time
        else:
            # Insert task to appropriate area in matrix
            self.matrix[important][urgent][task] = time
        return

    # Delete object from matrix
    def delete(self, task, important, urgent):
        self.matrix[important][urgent].pop(task)
        return

    # Deletes all tasks that have been scheduled (done)
    def deleteDone(self):
        for i, row in enumerate(self.matrix):
            for j, column in enumerate(row):
                self.matrix[i][j] = {k: v for (k, v) in column.items() if k not in self.done}
        return

    # Prints all tasks that could not be scheduled in the allocated time
    def leftToDo(self):
        if all(not dictionary for sub in self.matrix for dictionary in sub):
            return
        else:
            print("Left to do:")
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    self.printQuarter(i, j)
        return

    # Schedules tasks based on importannce
    def schedule(self, hours, start):

        # If tasks the user wanted to do are useless, reduce the amount of time needed to work
        if self.deletedTasks:
            for time in self.deletedTasks.values():
                hours = hours - time

        end = start + hours

        # While there's still time left and the dictionary is not empty...
        while start < end and not all(dictionary for sub in self.matrix for dictionary in sub):

            # ...loop through each task, print it out, and append it to the done
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    k = 0

                    # For each task
                    while k < len(self.matrix[i][j]):

                        # Schedule lunch at 1
                        if start == 13:
                            # Iterate time but not task and don't do rest of code
                            print("13:00 - Lunch")
                            start = start + 1
                            continue
                        # Prints
                        elif start < 10:
                            print("0" + str(start) + ":00" + " - " + list(self.matrix[i][j].keys())[k])
                            self.done.append(list(self.matrix[i][j].keys())[k])
                        else:
                            print(str(start) + ":00" + " - " + list(self.matrix[i][j].keys())[k])
                            self.done.append(list(self.matrix[i][j].keys())[k])

                        # Iterate time and task
                        start = start + list(self.matrix[i][j].values())[k]
                        k = k + 1

                        # If have reached the end, call deleteDone(), leftToDo(), and print deleted tasks.
                        if start >= end:
                            self.deleteDone()
                            self.leftToDo()
                            if len(self.deletedTasks) > 0:
                                print("We deleted: ")
                                print(*self.deletedTasks, sep=", ")
                            return
        # If there were no tasks
        else:
            print("No tasks to do. Well done!")
        return

    # Asks user to input tasks
    def inputTasks(self, workAmount, startTime):
        endTime = startTime + workAmount

        # Loops through until the user quits
        quitting = False
        while not quitting and startTime < endTime:

            # Gets valid task
            task = input("Enter a task name (or 'q' to quit): ")
            while len(task) <= 0:
                task = input("Enter a task name (or 'q' to quit): ")

            # Checks if the user wants to quit
            if task == "q":
                if startTime == endTime:
                    quitting = True
                    break
                else:
                    print("You'd better keep going, still some work left to do.")

            # Gets valid time for task
            while True:
                time = input("How long will this task take (in hours)?: ")
                try:
                    val = int(time)
                    if val >= 0 and (startTime + val) <= endTime and val <= 24:
                        startTime = startTime + val
                        break
                    else:
                        print(
                            "Please enter an appropriate number (positive, less than or equal to 24, and doesn't take you past the end time): ")
                except ValueError:
                    print("Amount must be a number, try again")

            time = int(time)

            # Gets whether the task in important and validates
            important = input("Is this task important? (yes/no): ")
            while important not in ("yes", "no"):
                important = input("Please enter yes/no: ")
            # Sets False (0) if yes and True (1) if no
            important = False if important == "yes" else True

            # Gets whether the task in urgent and validates
            urgent = input("Is this task urgent? (yes/no): ")
            while urgent not in ("yes", "no"):
                urgent = input("Please enter yes/no: ")
            # Sets False (0) if yes and True (1) if no
            urgent = False if urgent == "yes" else True

            # Inserts the task
            self.insert(task, time, important, urgent)
        return

    # Gets some initial inputs from the user, could add a lunch time and breaks variable
    def initialInputs(self):

        # Gets valid work time
        while True:
            workAmount = input("How long would you like to work today (in hours)?: ")
            try:
                val = int(workAmount)
                if val >= 0 and val <= 24:
                    break
                else:
                    print("Please enter a number greater than 0: ")
            except ValueError:
                print("Amount must be a number, try again")

        workAmount = int(workAmount)

        # Gets valid start time
        while True:
            startTime = input("When would you like to start (in hours)?: ")
            try:
                val = int(startTime)
                if val >= 0 and val <= 23 and (val + workAmount) <= 24:
                    break
                else:
                    print("Please enter a number greater than 0 that leaves enough time to complete your work: ")
            except ValueError:
                print("Amount must be a number, try again")

        startTime = int(startTime)
        return workAmount, startTime

    # Calls methods to set up prioritised schedule for the day
    def setup(self):
        workAmount, startTime = self.initialInputs()
        self.inputTasks(workAmount, startTime)
        self.schedule(workAmount, startTime)
        return


# Instantiates object and calls setup
eisenhower = Matrix()
eisenhower.setup()
