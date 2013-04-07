from communities.models import Community
from django.conf import settings
from django.db import models


class Issue(models.Model):
    community = models.ForeignKey(Community, related_name="issues")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="issues_created")

    title = models.CharField(max_length=300)
    abstract = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    calculated_score = models.IntegerField(default=0)

    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                                  related_name="issues_closed")

    def __unicode__(self):
        return self.title


class ProposalVoteValue(object):
    CON = -1
    NEUTRAL = 0
    PRO = 1

    CHOICES = (
                (CON, "Con"), 
                (NEUTRAL, "Neutral"), 
                (PRO, "Pro"),
               )


class ProposalVote(models.Model):
    proposal = models.ForeignKey("Proposal")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    value = models.PositiveIntegerField(choices=ProposalVoteValue.CHOICES)


class ProposalType(object):
    TASK = 1
    POLICY = 2
    RULE = 3
    ADMIN = 4

    CHOICES = (
                (TASK, "Task"), 
                (POLICY, "Policy"), 
                (RULE, "Rule"),
                (ADMIN, "Administrative"),
               )


class Proposal(models.Model):
    issue = models.ForeignKey(Issue, related_name="proposals")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="proposals_created")
    type = models.PositiveIntegerField(choices=ProposalType.CHOICES)

    title = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)

    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                                  related_name="proposals_assigned")
    due_by = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.title
