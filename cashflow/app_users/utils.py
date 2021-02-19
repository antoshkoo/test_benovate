from decimal import Decimal, ROUND_DOWN

from app_users.models import CustomUser


def sending_calc(sender, amount, recipients):
    amount = float(amount)
    if sender.tin in recipients:
        return {'status': 'You can\'t send money to yourself'}
    elif len(recipients) != len(set(recipients)):
        return {'status': 'TIN duplicated in recipients list'}
    elif sender.balance < amount:
        return {'status': 'Please charge balance'}
    elif CustomUser.objects.filter(tin__in=recipients).exists() is False:
        return {'status': f'One or more recipient not found'}
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
