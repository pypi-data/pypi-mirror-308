from artigen.Registry.Darn import Darn
import asyncio

async def test_list_darn():
    api_key = "BACJon+11hb4tR7GewlxMPzkTsLBvcfcyuGwdAlAuVQ2ImYCYL0ecdRR5GxwdYZOzzxLJ1shH3uJ3U4FY3EEQopJKooNHZ15QIDuhqKJ8WpFer4unBXOf8GshTZMwfgbbxLt+YExHG2i+ep3C7cR7Y8n0eMnHVN/u+pj/tS3XFfFnL+u/tUuDXqPk30r9bR9LC428JF7i0U6t+XwZB9k6w=="
    darn = Darn(api_key=api_key)
    # response = await darn.list_darn()
    # print(response)
    # darn_create= await darn.create_darn(name="sdk_hugging_check", token="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", dataset="qq8933/OpenLongCoT-Pretrain", darn_type="huggingface")
    # print(darn_create)
    # darn_create = await darn.update_darn(
    #     name="SDK_1001",
    #     file_paths=["/Users/surajsingh/Downloads/09738562-8C7D-42C5-B8B4-D0B341E2FA96.jpg"]
    # )
    # print(darn_create)
    #
    # darn_create = await darn.create_darn(
    #     name="SDK_local_check", dataset=["/Users/surajsingh/Desktop/Screenshot 2024-10-07 at 11.30.06.png", "/Users/surajsingh/Desktop/Screenshot 2024-09-27 at 16.53.25.png"], darn_type="local")
    # print(darn_create)

    darn_create = await darn.create_darn(
        name="SDK_bigquery_check_1", projectName="atndataset", credentialFile="/Users/surajsingh/Downloads/atndataset-2665e4bf385a.json",
        darn_type="bigquery", dataset=["Ecommerce.adjustment_details", "telecom.account_information", "Ecommerce.reviews_0"])
    print(darn_create)
    # # darn_delete=await darn.delete_darn(name="SDK_101")
    # print(darn_delete)
asyncio.run(test_list_darn())