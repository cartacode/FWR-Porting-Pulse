from porting_pulse import Porting_puls
import completion_time
import sys

if __name__ == "__main__":

    """just for pulling reports"""

    p=Porting_puls()
    col = p.find_col()
    p.report_plot()
    p.report_month()
    p.report_vip_comp()
    exec("completion_time")