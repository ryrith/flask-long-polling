import time


def updater(message, **kwargs):
    print message


def first_logic(param1,param2,**kwargs):
    from flask import session
    n = session.get('n') or 0

    sid = kwargs.get('polling').get('sid')
    for i in range(100):
        n = n+1
        session['n'] = n
        time.sleep(0.1)
        updater('First (p1={p1},p2={p2}) - session.n = {n} - updating...{i}'.format(i=i, p1=param1, p2=param2,
                                                                                    n=session.get('n')), **kwargs)
    updater('success', finish=True, **kwargs)


def second_logic(id,name,**kwargs):
    sid = kwargs.get('polling').get('sid')
    for i in range(10):
        time.sleep(0.3)
        updater('Second (id={id},name={name}) - updating...{i}'.format(i=i, id=id, name=name), **kwargs)
    updater('success', finish=True, **kwargs)
