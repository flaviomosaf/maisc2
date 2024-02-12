from django.db import models

class Analytic(models.Model):
    message_raw = models.CharField(max_length=200, blank=True, null=True)
    message_with_ents = models.CharField(max_length=200, blank=True, null=True)
    priority = models.CharField(max_length=200, blank=True, null=True)
    tokens = models.CharField(max_length=200, blank=True, null=True)
    date  = models.CharField(max_length=200, blank=True, null=True)
    tokens_len = models.CharField(max_length=200, blank=True, null=True)
    host_sender = models.CharField(max_length=200, blank=True, null=True)
    host_receiver = models.CharField(max_length=200, blank=True, null=True)
    ip_sender = models.CharField(max_length=200, blank=True, null=True)
    ip_receiver = models.CharField(max_length=200, blank=True, null=True)
    start_processing = models.CharField(max_length=200, blank=True, null=True)
    finish_processing = models.CharField(max_length=200, blank=True, null=True)
    time_processing = models.CharField(max_length=200, blank=True, null=True)

    ents_posi = models.CharField(max_length=200, blank=True, null=True)
    ents_text = models.CharField(max_length=200, blank=True, null=True)
    ents_kind = models.CharField(max_length=200, blank=True, null=True)

    sentence_size = models.CharField(max_length=200, blank=True, null=True)
    sentence_list = models.CharField(max_length=200, blank=True, null=True)

    tot_noun = models.CharField(max_length=200, blank=True, null=True)
    tot_pron = models.CharField(max_length=200, blank=True, null=True)
    tot_punc = models.CharField(max_length=200, blank=True, null=True)
    tot_conj = models.CharField(max_length=200, blank=True, null=True)
    tot_num = models.CharField(max_length=200, blank=True, null=True)

    lst_noun = models.CharField(max_length=200, blank=True, null=True)
    lst_verb = models.CharField(max_length=200, blank=True, null=True)
    lst_adve = models.CharField(max_length=200, blank=True, null=True)
    lst_pron = models.CharField(max_length=200, blank=True, null=True)
    lst_adje = models.CharField(max_length=200, blank=True, null=True)
    lst_punc = models.CharField(max_length=200, blank=True, null=True)
    lst_conj = models.CharField(max_length=200, blank=True, null=True)
    lst_det = models.CharField(max_length=200, blank=True, null=True)
    lst_num = models.CharField(max_length=200, blank=True, null=True)
    lst_other = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.message_raw












