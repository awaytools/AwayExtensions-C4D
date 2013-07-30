CONTAINER AWDSkeletonAnimationTag
{
    NAME AWDSkeletonAnimationTag;

    GROUP 
    {    
        BOOL AWDSKELETON_EXPORT{}
        STRING AWDSKELETON_NAME { }
        BOOL CBOX_ALLFRAMES{}
	    GROUP
		{
			COLUMNS 2;
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