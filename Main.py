#!/home/kevin/anaconda3/bin/python3.7
from PyQt5 import QtCore, QtGui, QtWidgets
from crontab import CronTab
from mainwindow import Ui_MainWindow
import sys
import re
import subprocess
import uuid
from submit import Ui_submitDialog
from warning import Ui_warnDialog


class MainWindowUIClass(Ui_MainWindow):
    def __init__(self):
        '''Initialize the super class
        '''
        super().__init__()
        

    def setupUi(self,MW):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi(MW)
        self.set_signals()


    def debugPrint(self, msg):
        '''Print the message in the text edit at the bottom of the
        horizontal splitter.
        '''
        self.taskTextBrowser.clear()
        self.taskTextBrowser.append(msg)


    def debugPrint_1(self, msg):
        '''Print the message in the text edit at the bottom of the
        horizontal splitter.
        '''
        self.taskHelpTextBrowser.clear()
        self.taskHelpTextBrowser.append(msg)
        self.refreshFutures()


    def set_signals(self):
        self.editButton.clicked.connect(self.editSlot)
        self.taskBox.activated.connect(self.taskListSlot)
        self.cronSetButton.clicked.connect(self.setCronSlot)
        self.delButton.clicked.connect(self.deleteSlot)
        self.submitButton.clicked.connect(self.submitSlot)
        self.atSetButton.clicked.connect(self.atSetlot)
        self.addButton.clicked.connect(self.addSlot)
        self.taskListWidget.itemClicked.connect(self.setTask)
        self.pastListWidget.itemClicked.connect(self.setPresent)
        self.pastButton.clicked.connect(self.viewLog)
        self.presentListWidget.itemClicked.connect(self.setPresent)
        self.tabWidget.currentChanged.connect(self.refreshList)


    def atFormat(self, jobset):
        f_out = open('futures.log', 'w')
        for i in jobset:
            r = re.split("\s+\d+:\d+:\d+\s+", i)[0]
            e = re.search(r'^(\d+)\s*\w+\s+(\w+\s+\d+)$', r)
            g = re.search(r'^.*\s+(\d+:\d+):\d+\s+(\d+).*$', i)
            jobid = str(e.group(1))
            monthday = str(e.group(2))
            mhtime = str(g.group(1))
            year = str(g.group(2))
            getbot = subprocess.Popen('at -c %s' % jobid, stdout=subprocess.PIPE,
                shell=True).communicate()[0]
            getbot = getbot.decode("utf-8")
            ex = re.split("--robot\s+", getbot)[1]
            ex = re.sub(r'\n','', ex)
            f_out.write('at %s %s %s %s jobid: %s\n' % (mhtime, monthday, year, ex, jobid))
        f_out.close()


    def refreshFutures(self):
        f_out = open('futures.log', 'w')
        atqueue = subprocess.Popen('atq', stdout=subprocess.PIPE,
                shell=True).communicate()[0]
        checks = atqueue.decode("utf-8")
        checks = re.sub(r'\n$','', checks)
        jobset = checks.split('\n')
        try:
            self.atFormat(jobset)
        except:
            pass

        f_out = open('futures.log', 'a')
        users_cron = CronTab(user=True)
        users_cron.write('output.tab')

        with open('output.tab', 'r') as f:
            for line in f:
                try:
                    fi = re.match(r'^(.*)\s+DISPLAY=.*--robot\s+(.*)\s+#\s+(.*)$', line)
                    atc = fi.group(1)
                    robot = fi.group(2)
                    uf = fi.group(3)
                    f_out.write('%s %s jobid: %s\n' % (atc, robot, uf))
                except:
                    pass
        f_out.close()

        # move this soon

        self.presentListWidget.clear()
        with open('futures.log', 'r') as f_log:
            for r in f_log:
                r = re.sub(r'\n$', '', r)
                r = re.sub(r' $', '', r)
                self.presentListWidget.addItem(r)
                   
        
    def decisionDialog(self, msg):
        Dialog = QtWidgets.QDialog()
        self.ui = Ui_submitDialog()
        self.ui.setupUi(Dialog)
        self.ui.submitLabel.setText(msg)
        Dialog.show()
        signed = Dialog.exec_()
        if signed == Dialog.Accepted:
            return True
        else:
            return False


    def setCronSlot(self):
        if self.minCheckBox.isChecked() == True:
            minute = str('*')
        else:
            minute = str(self.minBox.value())

        if self.hourCheckBox.isChecked() == True:
            hour = str('*')
        else:
            hour = str(self.hourBox.value())
        
        if self.dayBox.currentText().startswith('Select'):
            dow = str('*')
        else:
            days = ['Mon ...', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            for i in range(len(days)):
                if self.dayBox.currentText() == days[i]:
                    dow = str(i)
        if self.monthBox.value() == 0:
            month = str('*')
        else:
            month = str(self.monthBox.value())
        if self.domBox.value() == 0:
            dom = str('*')
        else:
            dom = str(self.domBox.value())
        atc = ('%s %s %s %s %s' % (minute, hour, dom, month, dow))
        self.debugPrint_1(atc)
        

    def atSetlot(self):
        string = (str(self.dateTimeEdit.dateTime()))
        string2 = re.sub(r'^.*Time\(','',string)
        string2 = re.sub(r'\)$','',string2)
        datelist = string2.split(', ')
        datelist = list(map(int, datelist))
        months = [
                'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i in range(len(months)):
                if i+1 == datelist[1]:
                    MM = months[i]
                    atc = 'at %02d:%02d %s %02d %04d' % (
                        datelist[3], datelist[4], MM, datelist[2], datelist[0])

        if self.atComboBox.currentText().startswith('Select'):
            self.debugPrint_1(atc)
        else:
            atc = 'at now + %s %s' % (
                str(self.atSpinBox.value()), self.atComboBox.currentText())
            self.debugPrint_1(atc)


    def taskListSlot(self):
        if self.taskBox.currentText().startswith('Select'):
            self.taskListWidget.clear()
            self.debugPrint(str(''))
        else:
            select = str(self.taskBox.currentText())
            # this can functionize
            with open ('%s.txt' % select.lower(), 'r') as categ:
                for r in categ:
                    r = re.sub(r'\n$', '',r)
                    r = re.sub(r' $', '',r)
                    self.taskListWidget.addItem(r)


    def setTask(self,item):
        robot = str(item.text())
        self.debugPrint("%s" % robot) 


    def submitSlot(self):
        robot = self.taskTextBrowser.toPlainText()
        robot = re.sub(r'\n$', '', robot)
        atc = self.taskHelpTextBrowser.toPlainText()
        atc = re.sub(r'\n$', '', atc)
        if atc is '' or robot is '':
            Dialog1 = QtWidgets.QDialog()
            pop_ui = Ui_warnDialog()
            pop_ui.setupUi(Dialog1)
            Dialog1.show()
            Dialog1.exec_()
        else:
            signed = self.decisionDialog('%s %s' % (atc, robot))
            if signed == True:
                if atc.startswith('at'):
                    self.atInject(atc, robot)
                else:
                    self.cronInject(atc, robot)


    def pathFix(self, robot):
        path = str('/home/kevin/PycharmProjects/robots')
        runstring = 'DISPLAY=:0 python %s/run.py --robot %s' % (path, robot)
        print (runstring)

        return runstring


    def cronInject(self, atc, robot):
        uf = str(uuid.uuid4().hex)
        runstring = self.pathFix(robot)
        users_cron = CronTab(user=True)
        job = users_cron.new(command = runstring, comment = uf)
        job.setall(atc)
        users_cron.write(user=True)


    def atInject(self, atc, robot):
        path = str('/home/kevin/PycharmProjects/robots')
        python_path = str ('PATH=/home/kevin/anaconda3/bin:$PATH')
        runstring = self.pathFix(robot)
        filestring = str('%s/%s/input.at' % (path, robot))
        at_f = open('%s' % filestring, 'w')
        at_f.write('%s\n%s\n' % (python_path, runstring))
        at_f.close()
        subprocess.Popen('%s -f %s' % (atc, filestring),
                shell=True).communicate()


    def viewLog(self):
        litem = self.setPresent(self.pastListWidget.currentItem())
        if litem is False:
            pass
        else:
            dex = self.presentListWidget.currentRow()
            date = litem.split(': ')[1]
            logdate = date.split(' ')[0]
            month, day, year = logdate.split('/')
            lpath = str('/var/www/tests1/logs/20')  # current logpath
            string = str('%s%s/%s/%s/%s.log' % (lpath, year, month, day, day))
            signed = self.decisionDialog(
                    'View this log ? %s %s 20%s' %
                    (day, month, year))
            if signed == True:
                try:
                    self.pastListWidget.clear()

                    with open('%s' % string, 'r') as h_log:
                        for r in h_log:
                            r = re.sub(r'\n$', '', r)
                            r = re.sub(r' $', '', r)
                            self.pastListWidget.addItem(r)
                except:
                    pass


    def setPresent(self, item):
        try:
            litem = str(item.text())
            litem = re.sub(r'\n$', '', litem)
            return litem
        except:
            return False


    def addSlot(self):
        self.tabWidget.setCurrentIndex(0)


    def atReject(self, uf):
        atdel = subprocess.Popen('atrm %s' % uf, stderr=subprocess.PIPE,
                shell=True).communicate()[1]
        checks = atdel.decode("utf-8")
        try:
            checked = re.search(r'^.*Cannot\s+find\s+jobid\s+(\d+)$', checks)
            jobid = str(checked.group(1))
            print ('jobid %s missing from user atq' % jobid)
        except:
            pass


    def cronReject(self, uf):
        try:
            path = str('/home/kevin/PycharmProjects/robots')
            users_cron = CronTab(user=True)
            users_cron.remove_all(comment=uf)
            users_cron.write(user=True)
        except:
            print ('Job not in user crontab with id: %s' % uf)


    def deleteSlot(self):
        litem = self.setPresent(self.presentListWidget.currentItem())
        if litem is False:
            pass
        else:
            place = re.search(r'^(.*)\s+(\w+)\s+jobid:\s+(.*)$', litem)
            atc = str(place.group(1))
            robot = str(place.group(2))
            uf = str(place.group(3))
            signed = self.decisionDialog(
                    'This will delete: %s %s?' % (atc, robot))
            if signed == True:
                if atc.startswith('at'):
                    self.atReject(uf)
                else:
                    self.cronReject(uf)
                self.refreshFutures()


    def editSlot(self):
        litem = self.setPresent(self.presentListWidget.currentItem())
        if litem is False:
            pass
        else:
            place = re.search(r'^(.*)\s+(\w+)\s+jobid:\s+(.*)$', litem)
            atc = str(place.group(1))
            robot = str(place.group(2))
            uf = str(place.group(3))
            signed = self.decisionDialog(
                    'This will delete: %s %s and pass variables to Tasks?'
                    % (atc, robot))
            if signed == True:
                if atc.startswith('at'):
                    self.atReject(uf)
                else:
                    self.cronReject(uf)
                self.refreshFutures()

                self.debugPrint(robot)
                self.debugPrint_1(atc)
                self.tabWidget.setCurrentIndex(0)

    
    def refreshList(self):
        tab = self.tabWidget.currentIndex()
        if tab == 1: 
            self.pastListWidget.clear()
            with open('history.log', 'r') as h_log:
                for r in h_log:
                    r = re.sub(r'\n$', '', r)
                    r = re.sub(r' $', '', r)
                    self.pastListWidget.addItem(r)
        if tab == 2:
            self.refreshFutures()


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    ui.exitButton.clicked.connect(MainWindow.close)
    ui.actionExit.triggered.connect(MainWindow.close)
    MainWindow.show()
    sys.exit(app.exec_())

main()
