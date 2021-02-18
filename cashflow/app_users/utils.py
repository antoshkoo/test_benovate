from decimal import Decimal, ROUND_DOWN

from app_users.models import CustomUser


def check_recipients(recipients, sender):
    if sender.tin in recipients:
        return {'status': 'You can\'t send money to yourself'}
    elif len(recipients) != len(set(recipients)):
        return {'status': 'TIN duplicated in recipients list'}
    else:
        unavailable_list = []

        for recipient in recipients:
            if CustomUser.objects.filter(tin=recipient).exists() is False:
                unavailable_list.append(recipient)

        if len(unavailable_list) > 0:
            return {'status': f'Recipient not found - {unavailable_list}'}
        else:
            return True


def sending_calc(sender, amount, recipients):
    if sender.balance < amount:
        return {'status': 'Please charge balance'}

    else:
        total_recipients = len(recipients)
        personal_sum = Decimal(str(amount / total_recipients)).quantize(Decimal("1.00"), ROUND_DOWN)
        total_sum = personal_sum * total_recipients
        new_balance = sender.balance - total_sum
        charge_back = Decimal(str(amount)) - total_sum

        for recipient in recipients:
            recipient = CustomUser.objects.get(tin=recipient)
            recipient.balance += personal_sum
            recipient.save()

        sender.balance = new_balance
        sender.save()

        return {
            'status': 'Money was send',
            'personal_sum': personal_sum,
            'total_sum': total_sum,
            'balance': new_balance,
            'charge_back': charge_back,
        }
