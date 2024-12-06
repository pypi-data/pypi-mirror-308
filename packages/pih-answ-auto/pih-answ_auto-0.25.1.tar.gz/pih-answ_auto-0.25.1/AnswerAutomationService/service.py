import ipih

from pih import A
from pih.tools import v, jnl, BitMask as BM
from AnswerAutomationService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


class ANSWER_TYPE:

    VISIT = 1
    TAX_CERTIFICATE = 2
    VISIT_MODIFICATION = 4
    HOW_TO_GET = 8
    OTHER_QUESTION = 16
    NEW_VISIT = 32


def start(as_standalone: bool = False) -> None:

    from pih.collections import (
        Message,
        PolibasePerson,
        WhatsAppMessage,
        PolibasePersonVisitDS as PPVDS,
        PolibasePersonNotificationConfirmation as PPNC,
    )

    from pih import serve, subscribe_on
    from pih.tools import j, js, ne, nn, one, nnt, ParameterList

    SENDER: str = A.D.get(A.CT_ME_WH_W.Profiles.CALL_CENTRE)

    def polibase_person_name_format(value: str, polibase_person: PolibasePerson) -> str:
        return value.format(name=A.D.to_given_name(polibase_person))

    def server_call_handler(sc: SC, pl: ParameterList) -> bool | None:
        if sc == SC.send_event:
            event: A.CT_E = A.D_Ex_E.get(pl)
            if event == A.CT_E.WHATSAPP_MESSAGE_RECEIVED:
                whatsapp_message: WhatsAppMessage | None = A.D_Ex_E.whatsapp_message(pl)
                if ne(whatsapp_message):
                    sender: str = nnt(nnt(whatsapp_message).profile_id)
                    if sender == SENDER:
                        telephone_number: str = A.D_F.telephone_number_international(
                            nnt(nnt(whatsapp_message).sender)
                        )
                        notification_confirmation: PPNC | None = A.R_P_N_C.by(
                            telephone_number, sender
                        ).data
                        if (
                            ne(notification_confirmation)
                            and nnt(notification_confirmation).status == 2
                        ):
                            polibase_person_visit_ds: PPVDS | None = one(
                                A.R_P_V_DS.search(
                                    PPVDS(
                                        telephoneNumber=A.D_F.telephone_number(
                                            telephone_number
                                        )
                                    )
                                )
                            )
                            if nn(polibase_person_visit_ds):
                                pin: int = nnt(nnt(polibase_person_visit_ds).pin)
                                person: PolibasePerson = (
                                    PolibasePerson(
                                        pin,
                                        nnt(polibase_person_visit_ds).FullName,
                                        nnt(polibase_person_visit_ds).telephoneNumber,
                                    )
                                    if pin == A.CT_P.PRERECORDING_PIN
                                    else A.D_P.person_by_pin(pin)
                                )
                                if A.A_P_N_C.update(nnt(person.telephoneNumber), sender, 1):

                                    answer_type: int = 0

                                    message: str = v(nnt(whatsapp_message).message)

                                    if ne(message):
                                        for index, variants in enumerate(
                                            [
                                                A.S.get(item)
                                                for item in (
                                                    A.CT_S.POLIBASE_ANSWER_PERSON_TAX_CERTIFICATE_VARIANTS,
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_VISIT_MODIFICATION_VARIANTS,
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_HOW_TO_GET_VARIANTS,
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_VISIT_VARIANTS,
                                                )
                                            ],
                                        ):
                                            if A.D.has_one_of(message, variants):
                                                answer_type = BM.set_index(
                                                    answer_type, index + 1
                                                )

                                    if answer_type == 0:
                                        answer_type = (
                                            ANSWER_TYPE.OTHER_QUESTION
                                            if nn(message) and message.find("?") != -1
                                            else ANSWER_TYPE.VISIT
                                        )

                                    def send_message(
                                        value: str | None = None,
                                        image_url: str | None = None,
                                        location: tuple[float, float] | None = None,
                                    ) -> None:
                                        A.ME_WH_W_Q.add(
                                            Message(
                                                value,
                                                person.telephoneNumber,
                                                sender,
                                                image_url,
                                                location,
                                            )
                                        )

                                    if BM.has(answer_type, ANSWER_TYPE.VISIT):
                                        send_message(
                                            A.S_P_V.offer_telegram_bot_url_text(person)
                                        )
                                        send_message(
                                            A.S.get(A.CT_S.TELEGRAM_BOT_URL),
                                        )

                                    if BM.has(answer_type, ANSWER_TYPE.OTHER_QUESTION):
                                        send_message(
                                            polibase_person_name_format(
                                                A.S.get(
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_OTHER_QUESTION_TEXT
                                                ),
                                                person,
                                            )
                                        )

                                    if BM.has(answer_type, ANSWER_TYPE.TAX_CERTIFICATE):
                                        send_message(
                                            polibase_person_name_format(
                                                A.S.get(
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_TAX_CERTIFICATE_TEXT
                                                ),
                                                person,
                                            )
                                        )
                                        send_message(
                                            A.S.get(A.CT_S.TAX_CERTIFICATE_URL),
                                        )

                                    if BM.has(
                                        answer_type, ANSWER_TYPE.VISIT_MODIFICATION
                                    ):
                                        send_message(
                                            polibase_person_name_format(
                                                A.S.get(
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_VISIT_MODIFICATION_TEXT
                                                ),
                                                person,
                                            ),
                                        )

                                    if BM.has(answer_type, ANSWER_TYPE.NEW_VISIT):
                                        send_message(
                                            polibase_person_name_format(
                                                A.S.get(
                                                    A.CT_S.POLIBASE_PERSON_ANSWER_NEW_VISIT_TEXT
                                                ),
                                                person,
                                            ),
                                        )

                                    if BM.has(answer_type, ANSWER_TYPE.HOW_TO_GET):
                                        send_message(
                                            A.S.get(
                                                A.CT_S.POLIBASE_PERSON_ANSWER_HOW_TO_GET_TEXT
                                            ),
                                            location=A.CT.ADDRESS.LOCATION,
                                        )
                                        for index in range(4):
                                            send_message(
                                                A.S.get(
                                                    getattr(
                                                        A.CT_S,
                                                        j(
                                                            (
                                                                A.CT_S.POLIBASE_PERSON_ANSWER_HOW_TO_GET_TEXT._name_,
                                                                index + 1,
                                                            )
                                                        ),
                                                    )
                                                ),
                                                image_url=A.PTH.APP_DATA.LOCATION_IMAGE_PATH(
                                                    index + 1
                                                ),
                                            )
                                    A.E.polibase_person_answered(
                                        person,
                                        js(
                                            (
                                                message,
                                                "|",
                                                js(("Тип ответа:", answer_type)),
                                            )
                                        ),
                                    )
        return None

    def service_starts_handler() -> None:
        subscribe_on(SC.send_event)

    serve(
        SD,
        server_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
