from googlesheet import Sheet
import pandas as pd
import datetime
import pytz
class Bot():
    def __init__(self):
        self.MGE = [180,90,60,50,40,30,20,20,20,20,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
        self.max = 15
        self.data = {
                "Top" : [],
                "DiscordID" : [],
                "PlayerID" : [],
                "Coins" : []
            }
        self.title = ""
        self.sTime = ""
        self.eTime = ""
        self.hTop = ""
        self.lTop = ""
        self.states = ""
    def help(self):
        detial=  {
            "mge" : "MGE Auction: .mge yourID coins . EX: .mge 123456 123",
            "rank" : "Check Top MGE Auction: .rank"
        }
        detial = self.mdConvert(detial)
        return detial

    def bid(self,message):
        self.states = self.check(message)
        ggSheet = Sheet()
        ggSheet.writeData(self.title,self.Top)
        bidContent = {
            "Title" : self.title,
            "Start Time" : self.sTime,
            "End Time" : self.eTime,
            "Hight Top" : self.hTop,
            "Low top" : self.lTop,
            "States": self.states,
        }
        detial= self.mdConvert(bidContent)
        return detial
    def mdConvert(self, data):
        tmp = []
        for key, value in data.items():
            tmp.append(f"- **{key}:** {value}")
        result= '\n'.join(tmp)
        return result
    def statuss(self):
        self.updateDataBase()
        tmpdf = self.Top.head(min(self.max, len(self.Top)))
        del tmpdf['DiscordID']
        detial= tmpdf.to_markdown(index=False, tablefmt ="jupyter")
        return detial

    def check(self,message):
        ggSheet = Sheet()
        self.updateDataBase()
        uContent = str(message.content)
        self.listContent = uContent.split()
        self.discordUserId = str(message.author.id)
        print(len(self.listContent))
        if len(self.listContent)<3:
            return "Please check the entered command for accuracy and verify the coin's value for auction."
        self.UID = str(self.listContent[1])
        self.bidCoins = self.listContent[2]
        if  not self.bidCoins.isdigit():
            return "Please check the entered command for accuracy and verify the coin's value for auction."
        self.bidCoins = int(self.bidCoins)
        self.updateDataBase()
        #Kiểm tra thời gian có hợp lệ không. 
        if  not self.check_date_within_range(self.sTime , self.eTime):
            return "Auction period has ended or has not started"
        # kiểm tra ID có hợp lệ không?
        coinsTable = ggSheet.readData("Coins")
        if self.UID not in coinsTable["ID"].values:
            return "Error: ID not True. Check your ID and try again."
        
        # lấy tên và số coins hiện tại của người chơi.
        row = coinsTable.loc[coinsTable["ID"] == self.UID]
        self.PlayerName = row["Name"].values[0]
        self.PlayerCoins = row["Coins"].values[0]
        if int(self.PlayerCoins) < int(self.bidCoins):
            return f"The current number of coins is not enough. \n {self.PlayerName} : {self.PlayerCoins}"
        # kiểm tra xem người chơi đã bid chưa.
        if self.UID in self.Top["PlayerID"].values:
            return self.update_coins(self.UID, self.discordUserId ,  self.bidCoins)
        else:
            return self.add_data(0,self.discordUserId,self.UID,self.bidCoins)

           

    def update_coins(self, player_id, discord_id, new_coins):
        for i in range(len(self.Top["PlayerID"])):
            if self.Top["PlayerID"][i] == player_id and self.Top["DiscordID"][i] == discord_id:
                self.Top["Coins"][i] = new_coins
                self.updateTop()
                return "Complete your auction update."
        return "You are not allowed to bid for another account."
    def add_data(self, top_value, discord_id, player_id, coins):
        data = {
            "Top": top_value,
            "DiscordID": discord_id,
            "PlayerID": player_id,
            "Coins": coins
        }
        self.Top.loc[len(self.Top)] = data
        self.updateTop()
        return "Done"
    def updateTop(self):
        self.Top = self.Top.sort_values('Coins', ascending=False)
        # Cập nhật giá trị vào cột "Top"
        self.Top['Top'] = range(int(self.hTop), int(self.hTop)+len(self.Top) + 1)[:len(self.Top)]
    def updateDataBase(self):
        ggSheet = Sheet()
        settingBot = ggSheet.readData("SettingBot")
        self.title = settingBot.columns.tolist()[1]
        self.sTime = settingBot[self.title].iloc[0]
        self.eTime = settingBot[self.title].iloc[1]
        self.hTop = settingBot[self.title].iloc[2]
        self.lTop = settingBot[self.title].iloc[3]
        worksheet_titles = [worksheet.title for worksheet in ggSheet.worksheet_list]
        if self.title not in worksheet_titles:
            ggSheet.createWorksheet(self.title)
            self.Top = pd.DataFrame(self.data)
            ggSheet.writeData(self.title,self.Top)
        else:
            self.Top = ggSheet.readData(self.title)
            self.Top["DiscordID"] = self.Top["DiscordID"].astype(str)
            self.Top["PlayerID"] = self.Top["PlayerID"].astype(str)
            self.Top["Coins"] = self.Top["Coins"].astype(int)
                
    def check_date_within_range(self, date1, date2):
        current_date = datetime.datetime.now(pytz.utc).date()
        date1 = datetime.datetime.strptime(date1, "%d/%m/%Y").date()
        date2 = datetime.datetime.strptime(date2, "%d/%m/%Y").date()

        if date1 <= current_date <= date2:
            return True
        else:
            return False
        


if __name__ == "__main__":
    ggSheet = Sheet()
    settingBot = ggSheet.readData("SettingBot")
    title = settingBot.columns.tolist()[1]
    sTime = settingBot[title].iloc[0]
    eTime = settingBot[title].iloc[1]
    hTop = settingBot[title].iloc[2]
    lTop = settingBot[title].iloc[3]
    print(title)
    print(sTime)
    print(eTime)
    print(hTop)
    print(lTop)