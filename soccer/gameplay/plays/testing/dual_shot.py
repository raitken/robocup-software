import robocup
import play
import behavior
import constants
import main
import skills.move
import skills.capture
import tactics.coordinated_pass
import enum

class Dual_Shot(play.Play):

    KickPower = 30

    class State(enum.Enum):
        setup = 1 #2 in position, 1 fetches
        passing = 2

    def __init__(self):
        super().__init__(continuous=True)

        self.add_state(Dual_Shot.State.setup, 
            behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start,
            Dual_Shot.State.setup,
            lambda:True, 'immediately')

        self.add_transition(Dual_Shot.State.setup, 
            Dual_Shot.State.passing,
            lambda: self.all_subbehaviors_completed(),
            'all subbehaviors completed')



        self.shooting_points = [
            robocup.Point(constants.Field.Width/4.0,constants.Field.Length*3/4.0),
            robocup.Point(-constants.Field.Width/4.0,constants.Field.Length*3/4.0)
        ]

    def all_subbehaviors_completed(self):
        for bhvr in self.all_subbehaviors():
            if not bhvr.is_done_running():
                return False
        return True

        return all([bhvr.is_done_running() for bhvr in self.all_subbehaviors()])

    def on_enter_setup(self):
        self.add_subbehavior(skills.move.Move(self.shooting_points[0]), 'move1')
        self.add_subbehavior(skills.move.Move(self.shooting_points[1]), 'move2')
        self.add_subbehavior(skills.capture.Capture(), 'capture')


    def on_exit_setup(self):
        self.remove_all_subbehaviors()

    def on_enter_passing(self):
        # kickFrom = min(self.shooting_points,
        #     key=lambda pt: pt.dist_to(main.ball().pos))
        # kickFromIdx = self.shooting_points.index(kickFrom)
        # kickToIdx = (kickFromIdx + 1) % len(self.shooting_points)
        # kickToPt = self.shooting_points[kickToIdx]
        line0 = robocup.Segment(
                self.shooting_points[0]-0.1,
                self.shooting_points[0]+0.1)
        line1 = robocup.Segment(
                self.shooting_points[1]-0.1,
                self.shooting_points[1]+0.1)
        if shot.eval_shot(main.ball().pos, line0) > shot.eval_shot(main.ball().pos, line1):
            self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.shooting_points[0]),
                'pass')
        else:
            self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.shooting_points[1]),
                'pass')
        # kickTo = max(shot.eval_shot(main.ball().pos, self.shooting_points[0]), 
        #     shot.eval_shot(main.ball().pos, self.shooting_points[1]),
        #     key=lambda pt: pt.dist_to(main.ball().pos))
        # kickToIdx = self.shooting_points.index(kickTo)

        # self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(kickToPt),
        #     'pass')

    def on_exit_passing(self):
        self.remove_all_subbehaviors()

    def on_enter_scoring(self):
        self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(min(pt.dist_to(main.ball().pos))),
            'pass')

    def on_exit_winning(self):
        self.remove_all_subbehaviors()