#property copyright "Copyright 2024, Life Associate Japan Inc."
#property version   "1.00"
#property strict

#define    OBJ_HEAD              ( __FILE__ + "_" )
#define    MAGIC_NO              CS50

#include <stdlib.mqh>
#include <stderror.mqh>
#include <WinUser32.mqh>
#include <Original/convertToJpTime.mqh>
#include <Original/Notification_dev.mqh>

input int    MovingPeriod  = 21;
input int    MovingShift   = 0;

NotificationLD *notice;


struct struct_PositionInfo {
    int               ticket_no;
    int               entry_dir; 
    double            set_limit; 
    double            set_stop;
};

enum ENUM_ENTRY_SIGNAL {
    SIGNAL_NO = 0,
    SIGNAL_UP_CHANGE,
    SIGNAL_DOWN_CHANGE 
};

static struct_PositionInfo  _StPositionInfoData; 

//+------------------------------------------------------------------+
//| OnInit Expert initialization function
//+------------------------------------------------------------------+
int OnInit()
{    
    
    notice = new NotificationLD();
    
    return( INIT_SUCCEEDED ); 
}


//+------------------------------------------------------------------+
//| OnDeinit Expert deinitialization function
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {

    if ( IsTesting() == false ) {
        ObjectsDeleteAll(
                        0,
                        OBJ_HEAD 
                       );
    }

    delete(notice);
   
  }
//+------------------------------------------------------------------+
//| Expert tick function
//+------------------------------------------------------------------+
void OnTick()
  {

    TaskPeriod();

  }

void TaskPeriod() {
    static    datetime s_lasttime;
    datetime temptime    = iTime( Symbol(), Period() ,0 );

    if ( temptime == s_lasttime ) { 
        return; 
    }
    s_lasttime = temptime;

    ENUM_ENTRY_SIGNAL temp_signal; 
    temp_signal = EntrySignalJudge(); 
}


ENUM_ENTRY_SIGNAL EntrySignalJudge(){
    
    ENUM_ENTRY_SIGNAL ret = SIGNAL_NO;

    double H1_open_USDJPY; 
    double H1_close_USDJPY;
    double H4_open_USDJPY;
    double Day_open_USDJPY;

    datetime now_time = convertToJapanTime();
    int      now_hour  = TimeHour(  now_time  );
    int      now_index  = now_hour-7;

        if ( now_hour >= 0 && now_hour <= 6 ) {
             now_index  = (now_hour+24)-7;
}

    H1_open_USDJPY = iOpen(
             "USDJPY",
             PERIOD_H1,
             0);

    H4_open_USDJPY = iOpen(
             "USDJPY",
             PERIOD_H4,
             0);

    Day_open_USDJPY = iOpen(
             "USDJPY",
             PERIOD_D1,
             0);

    H1_close_USDJPY = iClose(
             "USDJPY",
             PERIOD_H1,
             9);

    if ( now_hour == 6 || now_hour == 7 ) {

    int highestBar_USDJPY = iHighest("USDJPY", PERIOD_H1, MODE_HIGH,24, 0);
    double highestRate_USDJPY = iHigh( "USDJPY", PERIOD_H1, highestBar_USDJPY);
    datetime highestTime_USDJPY = iTime( "USDJPY", PERIOD_H1, highestBar_USDJPY);
    int lowestBar_USDJPY = iLowest("USDJPY", PERIOD_H1, MODE_LOW, 24, 0);
    double lowestRate_USDJPY = iLow( "USDJPY", PERIOD_H1, lowestBar_USDJPY);
    datetime lowestTime_USDJPY = iTime( "USDJPY", PERIOD_H1, lowestBar_USDJPY);

    if ( lowestTime_USDJPY <= highestTime_USDJPY ) {

     notice.sendMessage(
    "\nUSDJPY daily log info " +(string)TimeToStr(  now_time  )
     + "\nDaily Volatility: "        + (string)NormalizeDouble( highestRate_USDJPY - lowestRate_USDJPY,4 )+"yen"
     + "\nPrevious Lowest rate: "     + (string)( lowestRate_USDJPY )
     + "\nPrevious Lowest time: "  + (string)( TimeToStr( lowestTime_USDJPY ) )
     + "\nPrevious Highest rate: "     + (string)( highestRate_USDJPY )
     + "\nPrevious Highest time: "  + (string)( TimeToStr( highestTime_USDJPY ) )
     );

     notice.sendChartScreenDay();
     
     Sleep(SLEEP_SEC * 1000);
     
     notice.sendChartScreen();
     
    } else if ( lowestTime_USDJPY >= highestTime_USDJPY ) {

     notice.sendMessage(
    "\nUSDJPY daily log info " +(string)TimeToStr(  now_time  )
     + "\nDaily Volatility: "        + (string)NormalizeDouble( lowestRate_USDJPY - highestRate_USDJPY,4 )+"yen"
     + "\nPrevious Highest rate: "     + (string)( highestRate_USDJPY )
     + "\nPrevious Highest time: "  + (string)( TimeToStr( highestTime_USDJPY ) )
     + "\nPrevious Lowest rate: "     + (string)( lowestRate_USDJPY )
     + "\nPrevious Lowest time: "  + (string)( TimeToStr( lowestTime_USDJPY ) )
     );

     notice.sendChartScreenDay();
     
     Sleep(SLEEP_SEC * 1000);
     
     notice.sendChartScreen();
     
    }

  }
     if(  (H1_open_USDJPY - H1_close_USDJPY >= 0.20)
    ) {

        ret = SIGNAL_UP_CHANGE;

    }

    else if ( (H1_open_USDJPY - H1_close_USDJPY <= -0.20)
    ) {

        ret = SIGNAL_DOWN_CHANGE;

    }

    return ret;
}


//+------------------------------------------------------------------+
