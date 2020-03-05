
{
  "modified": "Sun Jan 08 2017 22:24:46 GMT+0900 (JST)",
  "api": [{
      "prefix": "global",
      "version": null,
      "resources": {
        "LangSetFetch": {
          "requireKey": false,
          "comment": "lang set fetch.",
          "path": "/nhkworld/assets/langset/{opt_lang}.json",
          "locationParams": [{
            "paramName": "opt_lang",
            "require": true
          }]
        }
      }
    },
    {
      "prefix": "ml",
      "version": null,
      "resources": { }
    },
    {
      "prefix": "news",
      "version": "v6a",
      "resources": {
        "Fetch": {
          "requireKey": false,
          "comment": "get news detail",
          "path": "/nhkworld/data/{lang}/news/{Id}.json",
          "locationParams": [{
            "paramName": "Id",
            "require": true
          }]
        },
        "DataFetch": {
          "requireKey": false,
          "comment": "get news detail from static file",
          "path": "/nhkworld/data/{lang}/news/{Id}.json",
          "locationParams": [{
            "paramName": "Id",
            "require": true
          }]
        },
        "ListFetch": {
          "requireKey": false,
          "comment": "news list api",
          "path": "/nhkworld/data/en/news/all.json",
          "locationParams": []
        },
        "RankingFetch": {
          "requireKey": false,
          "comment": "news list api",
          "path": "/nhkworld/data/en/news/{time}.json",
          "locationParams": [{
            "paramName": "time",
            "require": true
          }]
        },
        "ArchiveFetch": {
          "requireKey": false,
          "comment": "news archive list api",
          "path": "/nhkworld/data/en/news/archive.json",
          "locationParams": []
        },
        "VideoFetch": {
          "requireKey": true,
          "comment": "news Video Fetch",
          "path": "pg/{version}/info/{lang}/newsvideos/{Id}.json",
          "locationParams": [{
            "paramName": "Id",
            "require": true
          }]
        },
        "VideoList": {
          "requireKey": true,
          "comment": "news video list",
          "path": "pg/{version}/list/{lang}/newsvideos/all/all.json",
          "locationParams": []
        },
        "CatVideoList": {
          "requireKey": true,
          "comment": "news video list by category",
          "path": "pg/{version}/list/{lang}/newsvideos/all/{CategoryName}.json",
          "locationParams": [{
            "paramName": "CategoryName",
            "require": true
          }]
        },
        "BannerFetch": {
          "requireKey": false,
          "comment": "news banner fetch",
          "path": "/nhkworld/data/{lang}/banner/news.json",
          "locationParams": []
        },
        "MLListFetch": {
          "requireKey": true,
          "comment": "news list multi language.",
          "path": "rdnewsweb/{version}/{lang}/headline/list.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        },
        "MLOutlineFetch": {
          "requireKey": true,
          "comment": "news list multi language.",
          "path": "rdnewsweb/{version}/{lang}/outline/list.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        },
        "MLFetch": {
          "requireKey": true,
          "comment": "news list multi language.",
          "path": "rdnewsweb/v6a/{lang}/detail/{Id}.json",
          "locationParams": [{
              "paramName": "version",
              "default": "v6a"
            },
            {
              "paramName": "Id",
              "require": true
            }
          ]
        },
        "MLArchiveFetch": {
          "requireKey": false,
          "comment": "ML news archive list api",
          "path": "/nhkworld/data/{lang}/news/archive.json",
          "locationParams": []
        },
        "TsunamiFetch": {
          "requireKey": false,
          "comment": "tusnami api",
          "path": "/nhkworld/data/en/news/tsunami.json",
          "locationParams": []
        },
        "BreakingFetch": {
          "requireKey": false,
          "comment": "breaking news api",
          "path": "/nhkworld/data/en/news/breaking_en.json",
          "locationParams": []
        },
        "EditorsListFetch": {
          "requireKey": false,
          "comment": "editors list",
          "path": "/nhkworld/data/{lang}/news/editors/editors_all.json",
          "locationParams": []
        },
        "WeeklyVideoListFetch": {
          "requireKey": false,
          "comment": "weekly video list",
          "path": "/nhkworld/data/{lang}/news/weekly_video/list.json",
          "locationParams": []
        },
        "WeeklyVideoFetch": {
          "requireKey": false,
          "comment": "weekly video list",
          "path": "/nhkworld/data/{lang}/news/weekly_video/{Id}.json",
          "locationParams": [{
            "paramName": "Id",
            "require": true
          }]
        },
        "DailyVideoListFetch": {
          "requireKey": false,
          "comment": "editors list",
          "path": "/nhkworld/data/{lang}/news/daily_video/list.json",
          "locationParams": []
        },
        "DailyVideoFetch": {
          "requireKey": false,
          "comment": "editors list",
          "path": "/nhkworld/data/{lang}/news/daily_video/{Id}.json",
          "locationParams": [{
            "paramName": "Id",
            "require": true
          }]
        },
        "MLVideoList": {
          "requireKey": false,
          "comment": "editors list",
          "path": "/nhkworld/data/{lang}/news/video_list.json",
          "locationParams": []
        }
      }
    },
    {
      "prefix": "radio",
      "version": "v6a",
      "resources": {
        "EpisodeFetch": {
          "requireKey": true,
          "comment": "fetch radio episode",
          "path": "rod/v6a/episode/{slug}/{onairDate}/{lang}.json",
          "locationParams": [{
              "paramName": "slug",
              "require": true
            },
            {
              "paramName": "onairDate",
              "require": true
            }
          ]
        },
        "EpisodeFetchTmp": {
          "requireKey": false,
          "comment": "fetch radio episode",
          "path": "/nhkworld/apibase/{lang}/radio/episodes/{OnairDate}_{Seq}_{Order}-{Slug}.json",
          "locationParams": [{
              "paramName": "Slug",
              "require": true
            },
            {
              "paramName": "OnairDate",
              "require": true
            },
            {
              "paramName": "Seq",
              "require": true
            },
            {
              "paramName": "Order",
              "require": true
            }
          ]
        },
        "ProgramFetch": {
          "requireKey": false,
          "comment": "fetch radio program",
          "path": "/nhkworld/data/{lang}/radio/program/{Slug}.json",
          "locationParams": [{
            "paramName": "Slug",
            "require": true
          }]
        },
        "ProgramListFetch": {
          "requireKey": true,
          "comment": "radio program list api",
          "path": "rdpg/v6a/{lang}.json",
          "locationParams": []
        },
        "EpisodeListFetch": {
          "requireKey": true,
          "comment": "episode live list.",
          "path": "repg/{version}/{lang}/latest.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        },
        "ComingSoon": {
          "requireKey": true,
          "comment": "coming soon",
          "path": "repg/{version}/{lang}/soon.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        },
        "ScheduleListFetch": {
          "requireKey": true,
          "comment": "episode schedule list.",
          "path": "repg/{version}/{lang}/schedule.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        },
        "ProgramScheduleFetch": {
          "requireKey": true,
          "comment": "program schedule",
          "path": "base/x2j/v1a/RJlive_program3.json",
          "locationParams": []
        },
        "BannerFetch": {
          "requireKey": false,
          "comment": "radio banenr",
          "path": "/nhkworld/data/{lang}/banner/radio_v2.json",
          "locationParams": []
        },
        "RODListFetch": {
          "requireKey": true,
          "comment": "rod fetch",
          "path": "rod/{version}/clip_list/{lang}.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        },
        "EpisodeListWithROD": {
          "requireKey": true,
          "comment": "episode list with rod.",
          "path": "rod/{version}/episode_list/{Slug}/{lang}.json",
          "locationParams": [{
              "paramName": "version",
              "default": "v6a"
            },
            {
              "paramName": "Slug",
              "require": true
            }
          ]
        },
        "Schedule24": {
          "requireKey": false,
          "comment": "schedule 24h",
          "path": "/nhkworld/resources/rj/schedule_24h.json",
          "locationParams": []
        },
        "NewsClip": {
          "requireKey": true,
          "comment": "news audio",
          "path": "rdonews/{version}/{lang}/news.json",
          "locationParams": [{
            "paramName": "version",
            "default": "v6a"
          }]
        }
      }
    },
    {
      "prefix": "top",
      "version": null,
      "resources": {}
    },
    {
      "prefix": "tv",
      "version": "v7a",
      "resources": {
        "EpisodeFetch": {
          "requireKey": false,
          "comment": "fetch tv episode",
          "path": "/nhkworld/data/{lang}/tv/episode/{Slug}/{OnairDate}_{Id}.json",
          "locationParams": [{
              "paramName": "Slug",
              "require": true
            },
            {
              "paramName": "OnairDate",
              "require": true
            },
            {
              "paramName": "Id",
              "require": true
            }
          ]
        },
        "EpisodeListFetch": {
          "requireKey": false,
          "comment": "fetch episode list",
          "path": "/nhkworld/data/{lang}/tv/episode_list/{Slug}.json",
          "locationParams": [{
            "paramName": "Slug",
            "require": true
          }]
        },
        "EpisodeWithMeta": {
          "requireKey": true,
          "comment": "episode with vod, pgm",
          "path": "tvepisode/v6a/detail/{slug}/{onairDate}_{id}.json",
          "locationParams": [{
              "paramName": "slug",
              "require": true
            },
            {
              "paramName": "onairDate",
              "require": true
            },
            {
              "paramName": "id",
              "require": true
            }
          ]
        },
        "EpisodeListWithMeta": {
          "requireKey": true,
          "comment": "episode list with vod, pgm",
          "path": "tvepisode/v6a/list/{slug}/all.json",
          "locationParams": [{
            "paramName": "slug",
            "require": true
          }]
        },
        "ProgramFetch": {
          "requireKey": false,
          "comment": "fetch tv program",
          "path": "/nhkworld/data/{lang}/tv/program/{Slug}.json",
          "locationParams": [{
            "paramName": "Slug",
            "require": true
          }]
        },
        "ProgramListFetch": {
          "requireKey": false,
          "comment": "tv program list api",
          "path": "/nhkworld/apibase/tv_programs_en.json",
          "locationParams": []
        },
        "CategoryListFetch": {
          "requireKey": false,
          "comment": "tv active category list ",
          "path": "/nhkworld/data/en/tv/tv_programs.json",
          "locationParams": []
        },
        "BannerFetch": {
          "requireKey": false,
          "comment": "radio banenr",
          "path": "/nhkworld/data/{lang}/banner/tv.json",
          "locationParams": []
        },
        "EPGBySlug": {
          "requireKey": true,
          "comment": "TV Episode Fetch by slug",
          "path": "epg/{version}/{region}/P{Slug}P.json",
          "locationParams": [{
            "paramName": "Slug",
            "require": true
          }]
        },
        "EPGFetch": {
          "requireKey": true,
          "comment": "EPG",
          "path": "epg/{version}/{region}/{Time}.json",
          "locationParams": [{
            "paramName": "Time",
            "default": "12h"
          }]
        },
        "EPGByID": {
          "requireKey": true,
          "comment": "EPG By id",
          "path": "epg/{version}/{region}/{Id}.json",
          "locationParams": [{
            "paramName": "Id",
            "require": true
          }]
        },
        "EPGEpisodeFetch": {
          "requireKey": true,
          "comment": "Episode from EPG",
          "path": "epg/{version}/{region}/{Pgm_id}-{Pgm_no}.json",
          "locationParams": [{
              "paramName": "Pgm_id",
              "require": true
            },
            {
              "paramName": "Pgm_no",
              "require": true
            }
          ]
        },
        "EPGByLife": {
          "requireKey": true,
          "comment": "EPG By Life Category",
          "path": "epg/{version}/{region}/LC{LifeCategory}.json",
          "locationParams": [{
            "paramName": "LifeCategory",
            "default": "00"
          }]
        },
        "HowtoWatch": {
          "requireKey": true,
          "comment": "",
          "path": "base/x2j/v1a/howtowatch_{watchLang}.json",
          "locationParams": [{
            "paramName": "watchLang",
            "default": "e"
          }]
        },
        "HowtoWatchUS": {
          "requireKey": true,
          "comment": "",
          "path": "base/x2j/v1a/howtowatch_{watchLang}_us.json",
          "locationParams": [{
            "paramName": "watchLang",
            "default": "e"
          }]
        },
        "RangeListFetch": {
          "requireKey": true,
          "comment": "Episode Fetch between range",
          "path": "epg/{version}/{region}/s{Start}-e{End}.json",
          "locationParams": [{
              "paramName": "Start",
              "require": true
            },
            {
              "paramName": "End",
              "require": true
            }
          ]
        }
      }
    },
    {
      "prefix": "vod",
      "version": "v7a",
      "resources": {
        "PickupList": {
          "requireKey": true,
          "comment": "vod pickup list",
          "path": "vodesdlist/{version}/pickup/all/{lang}/{mode}/all.json",
          "locationParams": [{
            "paramName": "mode",
            "default": "voice"
          }]
        },
        "EpisodeListFetch": {
          "requireKey": true,
          "comment": "vod episode list",
          "path": "vodesdlist/{version}/{mode}/{key}/{lang}/{l_mode}/{limit}.json",
          "locationParams": [{
            "paramName": "mode",
            "default": "all"
          }, {
            "paramName": "key",
            "default": "all"
          }, {
            "paramName": "lang",
            "default": "en"
          }, {
            "paramName": "l_mode",
            "default": "all"
          }, {
            "paramName": "limit",
            "default": "all"
          }]
        },
        "ProgramListFetch": {
          "requireKey": true,
          "comment": "program list",
          "path": "vodpglist/{version}/{lang}/{l_mode}/list.json",
          "locationParams": [{
            "paramName": "l_mode",
            "default": "voice"
          }]
        },
        "CategoryListFetch": {
          "requireKey": true,
          "comment": "category list",
          "path": "vodcatlist/{version}/{mode}/{lang}/{content_type}/list.json",
          "locationParams": [{
              "paramName": "version",
              "default": "v7a"
            },
            {
              "paramName": "mode",
              "default": "notzero"
            },
            {
              "paramName": "lang",
              "default": "en"
            },
            {
              "paramName": "content_type",
              "default": "ondemand"
            }
          ]
        },
        "EpisodeByCategoryListFetch": {
          "requireKey": true,
          "comment": "episode list by category.",
          "path": "vodesdlist/{version}/category/{Id}/{lang}/{l_mode}/all.json",
          "locationParams": [{
              "paramName": "Id",
              "require": true
            },
            {
              "paramName": "l_mode",
              "default": "voice"
            }
          ]
        },
        "EpisodeLifeListFetch": {
          "requireKey": true,
          "comment": "lf vod list",
          "path": "vodesdlist/{version}/life/all/{lang}/{l_mode}/all.json",
          "locationParams": [{
            "paramName": "l_mode",
            "default": "voice"
          }]
        },
        "EpisodeByProgramListFetch": {
          "requireKey": true,
          "comment": "episode by program id",
          "path": "vodesdlist/{version}/program/{pgm_gr_id}/{lang}/{l_mode}/all.json",
          "locationParams": [{
              "paramName": "pgm_gr_id",
              "require": true
            },
            {
              "paramName": "l_mode",
              "default": "voice"
            }
          ]
        },
        "EpisodeByCodeListFetch": {
          "requireKey": true,
          "comment": "episode by code",
          "path": "vodesdlist/{version}/episode/{EpisodeCode}/{lang}/{l_mode}/all.json",
          "locationParams": [{
              "paramName": "EpisodeCode",
              "require": true
            },
            {
              "paramName": "l_mode",
              "default": "voice"
            }
          ]
        },
        "EpisodeByMostWatchedListFetch": {
          "requireKey": true,
          "comment": "episode by code",
          "path": "vodesdlist/{version}/mostwatch/all/{lang}/{l_mode}/all.json",
          "locationParams": [{
            "paramName": "l_mode",
            "default": "voice"
          }]
        },
        "RecommendListFetch": {
          "requireKey": true,
          "comment": "vod pickup list",
          "path": "vodrecommend/{version}/{lang}/list.json",
          "locationParams": [{
            "paramName": "lang",
            "require": true
          }]
        },
        "ShortClipListFetch": {
          "requireKey": true,
          "comment": "vod short clip list",
          "path": "vodcliplist/{version}/{mode}/{key}/{lang}/{l_mode}/{limit}.json",
          "locationParams": [{
              "paramName": "lang",
              "require": true
            },
            {
              "paramName": "key",
              "require": true
            },
            {
              "paramName": "mode",
              "require": true
            },
            {
              "paramName": "l_mode",
              "default": "all"
            },
            {
              "paramName": "limit",
              "require": true
            }
          ]
        },
        "PlayListFetch": {
          "requireKey": true,
          "comment": "vod play list",
          "path": "vodplaylist/{version}/{lang}/{playlist_id}.json",
          "locationParams": [{
            "paramName": "lang",
            "require": true
          }, {
            "paramName": "playlist_id",
            "require": true
          }]
        },
        "TagListFetch": {
          "requireKey": true,
          "comment": "vod tag list",
          "path": "vodtaglist/{version}/{lang}/list.json",
          "locationParams": [{
            "paramName": "lang",
            "require": true
          }]
        }
      }
    },
    {
      "prefix": "rod",
      "version": "v7a",
      "resources": {
        "ProgramFetch": {
          "requireKey": true,
          "comment": "rod program fetch",
          "path": "rodpglist/{version}/{lang}/list.json",
          "locationParams": [{
            "paramName": "lang",
            "require": true
          }]
        },
        "EpisodeFetch": {
          "requireKey": true,
          "comment": "rod episode fetch",
          "path": "rodesdlist/{version}/{mode}/{key}/{lang}/{limit}.json",
          "locationParams": [{
            "paramName": "mode",
            "require": true
          }, {
            "paramName": "key",
            "require": true
          }, {
            "paramName": "lang",
            "require": true
          }, {
            "paramName": "limit",
            "require": true
          }]
        },
        "CategoryFetch": {
          "requireKey": true,
          "comment": "rod category fetch",
          "path": "rodcatlist/{version}/{mode}/{lang}/{content_type}/list.json",
          "locationParams": [{
              "paramName": "mode",
              "require": true
            }, {

              "paramName": "lang",
              "require": true
            },
            {

              "paramName": "content_type",
              "require": true
            }
          ]
        },
        "RecommendFetch": {
          "requireKey": true,
          "comment": "rod recommend fetch",
          "path": "rodrecommend/{version}/{lang}/list.json",
          "locationParams": [{
            "paramName": "lang",
            "require": true
          }]
        },
        "TagListFetch": {
          "requireKey": true,
          "comment": "rod tags list fetch",
          "path": "rodtaglist/{version}/{lang}/list.json",
          "locationParams": [{
            "paramName": "lang",
            "require": true
          }]
        }
      }
    },
    {
      "prefix": "zh",
      "version": "v7a",
      "resources": {
        "LiveEPGFetch": {
          "requireKey": true,
          "comment": "zvod live",
          "path": "zepg/{version}/{region}/{mode}.json",
          "locationParams": [{
            "paramName": "region",
            "default": "japan"
          }, {
            "paramName": "mode",
            "default": "now"
          }]
        }
      }
    }
  ]
}