CONTAINER AWDvertexAnimationTag
{
    NAME AWDvertexAnimationTag;

    GROUP 
    {  
        BOOL AWDSKELETON_EXPORT{}
        STRING AWDSKELETON_NAME { }
        LINK LINK_TARGETOBJ{}
        BOOL CBX_CAPTUREDEFORMER{}
        BOOL CBOX_LOOP{}
        BOOL CBOX_STITCH{}
	    GROUP
		{
			COLUMNS 2;
			STATICTEXT COMBO_ALLFRAMES_STR { }
			LONG COMBO_ALLFRAMES {                
                CYCLE
                {
                    COMBO_ALLFRAMES_ALL;
                    COMBO_ALLFRAMES_OBJECTKEYS;
                    COMBO_ALLFRAMES_TAGKEYS;
                    COMBO_ALLFRAMES_KEYNUM;
                }            
            }
            }
            STRING STRING_KEYFRAMER { }
            GROUP
            {
                COLUMNS 2;
                STATICTEXT REAL_KEYFRAME_STR { }
                REAL REAL_KEYFRAME { }	
            
			STATICTEXT COMBO_RANGE_STR { }
			LONG COMBO_RANGE {                
                CYCLE
                {
                    COMBO_RANGE_GLOBAL;
                    COMBO_RANGE_DOC;
                    COMBO_RANGE_PREVIEW;
                    COMBO_RANGE_CUSTOM;
                }            
            }
			STATICTEXT REAL_FIRSTFRAME_STR { }
			REAL REAL_FIRSTFRAME { }	
			STATICTEXT REAL_LASTFRAME_STR { }
			REAL REAL_LASTFRAME {}				
		} 
	}

}