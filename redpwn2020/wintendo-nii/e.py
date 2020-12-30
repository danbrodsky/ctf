import angr
p = angr.Project('./nii')
s = p.factory.entry_state()
sm = p.factory.simgr(s, veritesting=True)
sm.run()
