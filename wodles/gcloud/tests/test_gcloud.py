# Copyright (C) 2015, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute
# it and/or modify it under the terms of GPLv2

"""Unit tests for gcloud module."""

import sys
import os
import pytest
import runpy
from unittest.mock import patch
from argparse import Namespace

sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..'))
import exceptions


@pytest.mark.parametrize('parameters, exception', [
    ({'integration_type': 'type', 'credentials_file': None, 'max_messages': 1,
      'log_level': 1, 'prefix': '', 'store_true': False, 'delete_file': False,
      'only_logs_after': None, 'n_threads': 1},
     exceptions.GCloudIntegrationTypeError),

    ({'integration_type': 'pubsub', 'subscription_id': 'subscription_id',
      'project': 'project', 'credentials_file': None, 'max_messages': 1,
      'log_level': 1, 'prefix': '', 'store_true': False, 'delete_file': False,
      'only_logs_after': None, 'n_threads': 0},
     exceptions.GCloudPubSubNumThreadsError),

    ({'integration_type': 'pubsub', 'subscription_id': 'subscription_id',
      'project': 'project', 'credentials_file': None, 'max_messages': 0,
      'log_level': 1, 'prefix': '', 'store_true': False, 'delete_file': False,
      'only_logs_after': None, 'n_threads': 1},
     exceptions.GCloudPubSubNumMessagesError),

    ({'integration_type': 'pubsub', 'subscription_id': 'subscription_id',
      'project': 'project', 'credentials_file': None, 'max_messages': 1,
      'log_level': 1, 'prefix': '', 'store_true': False, 'delete_file': False,
      'only_logs_after': None, 'n_threads': 1},
     SystemExit),

    ({'integration_type': 'access_logs', 'credentials_file': None,
      'max_messages': 1, 'bucket_name': '', 'log_level': 1,
      'prefix': '', 'store_true': False, 'only_logs_after': None,
      'delete_file': False, 'n_threads': 1},
     exceptions.GCloudBucketNameError),

    ({'integration_type': 'access_logs', 'credentials_file': None,
      'max_messages': 1, 'bucket_name': 'bucket', 'log_level': 1,
      'prefix': '', 'store_true': False, 'only_logs_after': None,
      'delete_file': False, 'n_threads': 2},
     exceptions.GCloudBucketNumThreadsError),

    ({'integration_type': 'access_logs', 'credentials_file': None,
      'max_messages': 1, 'bucket_name': 'bucket', 'log_level': 1,
      'prefix': '', 'store_true': False,
      'only_logs_after': None, 'delete_file': False,
      'n_threads': 1},
     SystemExit),
])
def test_gcloud_ko(parameters, exception):
    """
    Test that the module will abort its execution when called
    with invalid parameters.

    Parameters
    ----------
    parameters : dict
        Dictionary that simulates the values that could have
        been introduced by the user.
    exception : Exception
        Exception that should be raised by the module.
    """
    with pytest.raises(exception), \
         patch('tools.get_script_arguments',
               return_value=Namespace(**parameters)), \
         patch('pubsub.subscriber.pubsub.subscriber.Client.from_service_account_file'), \
         patch('pubsub.subscriber.WazuhGCloudSubscriber.check_permissions'), \
         patch('pubsub.subscriber.WazuhGCloudSubscriber.process_messages'), \
         patch('buckets.bucket.storage.client.Client.from_service_account_json'), \
         patch('buckets.access_logs.GCSAccessLogs.process_data',
               return_value=0):
        runpy.run_module('gcloud.py')
