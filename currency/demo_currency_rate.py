from datetime import datetime
import currency_exchange_rate  as currency

def __get_million_seconds_elapsed__(start, end):
    delta = end - start
    return (delta.days * 24 * 60 * 60 + delta.seconds) * 1000 + delta.microseconds / 1000.0

def __get_respond_time__(converter, count):
    query_count = 10
    start = datetime.now()
    for i in range(0, query_count):
        converter.get_exchange_rate()
    end = datetime.now()    
    print 'avarage time is %d million second' %(__get_million_seconds_elapsed__(start, end)/query_count)

if __name__ == '__main__': 
    try:
        __get_respond_time__(currency.Fixer_provider("USD", "EUR", 5), 1)  
        __get_respond_time__(currency.Yahoo_provider("USD", "EUR", 5), 1)
    except currency.CurrencyUnavailableError:
        print "currency rate unavailable"
    except Exception:
        print "unexpected error!!!"
    else:
        print "success!"