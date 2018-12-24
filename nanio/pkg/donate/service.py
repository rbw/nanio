# -*- coding: utf-8 -*-

from nanio.pkg import NanioService


class DonationService(NanioService):
    def __init__(self, *args, **kwargs):
        super(DonationService, self).__init__(*args, **kwargs)
        self.donation = self.docs.Donation
        self.wallet = self.docs.Wallet

    async def node_send(self, command):
        data, _ = await self.pkg.node.svc.send(command)
        return data

    async def wallet_get(self):
        wallet = await self.wallet.find_one()
        if not wallet:
            data = await self.node_send({'action': 'wallet_create'})
            wallet = await self.wallet_set(data['wallet'])

        return wallet

    async def wallet_set(self, wallet_id):
        wallet = await self.wallet(wallet_id=wallet_id).commit()
        return wallet

    async def donation_create(self, req):
        ip_addr = req.remote_addr or req.ip

        pending = self.donation(
            message='test',
            address_from='xrb_3oecmxdde1eji5i9n8gpp3a6bno76etn7xuh35b7opjr15p6wif87ktwrqd6',
            address_to='ugh',
            pending=True,
            origin_addr=ip_addr
        )

        pending.commit()
        return self.donation.dump(pending)

    async def process_donation(self, req):
        # if self pending donate return 429
        # wallet_ref = await self.wallet_get()
        # account = await self.node_send({'action': 'payment_begin', 'wallet': wallet_ref['wallet_id']})
        # print(account)
        # print(await cursor.to_list(10))
        return await self.donation_create(req)


"""class DonationPending(Document):
    message = StringField(required=True, validate=Length(min=1, max=10))
    address_from = StringField(required=True, allow_none=False, validate=validate_address)
    address_to = StringField(required=True, allow_none=False, validate=validate_address)
    created_on = DateTimeField(missing=datetime.now())
    origin_addr = StringField(required=True, allow_none=False)"""

