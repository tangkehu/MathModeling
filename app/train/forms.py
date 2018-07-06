from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired
from ..models import TrainStudent, TrainTeam


class TrainMembersForm(FlaskForm):
    members = SelectMultipleField(label='小组成员', coerce=int, validators=[DataRequired(message='请选择成员')])

    def __init__(self, team, *args, **kwargs):
        super(TrainMembersForm, self).__init__(*args, **kwargs)
        self.members.choices = [(one.id, one.user.real_name) for one in TrainStudent.query.filter_by(
            school_id=current_user.school_id).order_by(
            TrainStudent.id.desc()).all() if not one.train_team or one.train_team_id == team.id]
        self.members.data = [one.id for one in team.train_student.all()]


class GradeManageForm(FlaskForm):
    children = SelectMultipleField(label='评分任务', validators=[DataRequired(message='请选择任务')], coerce=int)

    def __init__(self, team, *args, **kwargs):
        super(GradeManageForm, self).__init__(*args, **kwargs)
        self.children.choices = [(one.id, one.team_number+'组') for one in TrainTeam.query.filter_by(
            school_id=current_user.school_id).order_by(TrainTeam.id.desc()).all()]
        self.children.data = [one.child_team_id for one in team.children.all()]
