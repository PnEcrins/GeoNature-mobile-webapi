package org.osmdroid.views.overlay;

import org.osmdroid.ResourceProxy;
import org.osmdroid.views.MapView;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Point;

/**
 * Describe a Feature overlay.
 * 
 * @author <a href="mailto:sebastien.grimault@makina-corpus.com">S. Grimault</a>
 *
 */
public abstract class FeatureOverlay extends Overlay
{
	private String featureID;
	
	public FeatureOverlay(final Context ctx)
	{
		super(ctx);
	}

	public FeatureOverlay(final ResourceProxy pResourceProxy)
	{
		super(pResourceProxy);
	}
	
	@Override
	protected abstract void draw(final Canvas canvas, final MapView mapView, final boolean shadow);
	
	/**
	 * See if a given hit point is within the bounds of a {@link FeatureOverlay}.
	 *
	 * @param pHitPoint point to check
	 * @return true if the hit point is within the {@link FeatureOverlay}
	 */
	protected abstract boolean hitTest(final Point pHitPoint);
	
	public String getFeatureID()
	{
		return featureID;
	}

	public void setFeatureID(final String featureID)
	{
		this.featureID = featureID;
	}
}
