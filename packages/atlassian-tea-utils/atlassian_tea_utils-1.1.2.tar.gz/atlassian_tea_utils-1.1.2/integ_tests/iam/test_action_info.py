from atlassian_tea_utils.iam import IamInformation


def test_iam_information():
    ii = IamInformation()

    assert len(list(ii.generate_action_list)) > 100
    assert any(action == "s3:GetObject" for action in ii.expand_action("s3:get*"))
    assert all(action != "s3:UnknownAction" for action in ii.expand_action("s3:get*"))
