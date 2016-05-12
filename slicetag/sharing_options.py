#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# I edit this file locally, as VimwikiShareOptions.wiki.

# SHARING OPTIONS
ORIGIN_ROOT = '/run/media/mindey/ndisk/Data/vimwiki/'
SHARES_ROOT = '/run/media/mindey/ndisk/Data/pubwiki/'

PROVIDERS = {
 'GitHub': 'Github handle, with associated OAuth services identification',
 'Gmail' : 'Gmail email address, with associated OAuth services identification',
 'QQ': 'Tencent QQ number, with associated OAuth services identification',
 'Wechat': 'Tencent Wechat, with associated OAuth services identification',
 'Twitter': 'Twitter Inc. handle, with associated OAuth services identification',
 'Telegram': 'Telegram username or phone number',
 'GPG': 'GPG public key id',
 'Disk': 'Location to share to on the disk',
}

INDIVIDUALS = {
 'Public': {'Disk': ['/run/media/mindey/ndisk/Data/pubwiki/'],
 },
 'Mindey': {'GitHub': ['Mindey'],
            'Gmail': ['user@domain.com', 'user2@domain2.com'],
            'QQ': ['12345678'],
            'Telegram': ['@minx'],
            'Wechat': ['mindxyz'],
            'Twitter': ['Mindxyz'],
            'Disk': ['/run/media/mindey/ndisk/Data/vimwiki/w/mindey'],
 },
 'FriendX': {'Gmail': ['friendx@gmail.com', 'friendxmail2@gmail.com'],
             'Disk': ['/run/media/mindey/ndisk/Data/vimwiki/w/friendx'],
 },
 'FriendY': {'Wechat': ['friendy'],
             'Disk': ['/run/media/mindey/ndisk/Data/vimwiki/w/friendy'],
 }
}
# Note: while every INDIVIDUAL may have a a 'Disk' IDENTITY, we might
# want to use the same SHARES_ROOT to generate folder for each of them
# by concatenating SHARES_ROOT with the INDIVIDUALS dictionary key.

ORGANIZATIONS = {
 'ALL': ['Public'],
 'ME': ['Mindey'],
 'WE': ['FriendX',
        'Mindey'],
 'FRIENDS': ['Mindey',
             'FriendX',
             'FriendY',
             ],
}
